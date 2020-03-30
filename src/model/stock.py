from src.model.model import Model
from src.model.position import Position
from src.common.result import Result
from bson.objectid import ObjectId

class Stock(Model):
    """ An underlying position """
    collection = "stock"

    def __init__(self, trade):
        self.port = trade['port']
        self.stock = trade['stock']
        self.open = trade['open'] 
        self.closed = trade['closed']
        self.proceeds = trade['proceeds']
        self.commission = trade['commission']
        self.cash = trade['cash']
        self._id = trade['_id']

    @classmethod
    def new(cls, trade):
        # create a new stock to add its first trade
        return cls({
            '_id': ObjectId(),
            'port': trade.port, 
            'stock': trade.stock,
            'open': [],
            'closed': [],
            'proceeds': 0.0,
            'commission': 0.0,
            'cash': 0.0,
            }).create()

    @classmethod
    def get(cls, port, stock):
        """ Override model's get to use the stock name instead of _id """
        return cls.read({'port': port, 'stock': stock})

    def add(self, trade):
        """ Add this trade to a new or existing position """
        if trade.symbol in self.open: # Symbol has a position already e.g stock, option etc
            position = Position.get(trade.port, trade.symbol)
            position.add(trade)
            result = "CHANGED"
        else: # There are no positions on this symbol yet
            position = Position.new(trade)
            self.open.append(position.symbol)
            result = "OPENED"

        if position.closed:
            self.closed.append(position.symbol)
            self.open.remove(position.symbol)
            self.proceeds += position.proceeds
            self.commission += position.commission
            self.cash += position.cash
            result = "CLOSED"

        self.update()
        return result

    def is_flat(self):
        return self.open

    # def get_open_positions(self):
    #     return [Position.get(id) for id in self.open]

    # def get_closed_positions(self):
    #     return [Position.get(id) for id in self.closed]

    # def get_positions(self):
    #     positions = self.open + self.closed
    #     return [Position.get(id) for id in positions]
