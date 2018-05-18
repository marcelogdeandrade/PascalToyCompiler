# My module
class Id(object):
    cur_id = 0

    @staticmethod
    def getNewId():
        Id.cur_id += 1
        return Id.cur_id
