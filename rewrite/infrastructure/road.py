from lane import Lane

class Road:
    def __init__(self, from_vertex, to_vertex, length, lanes = 1, speed_limit = 50, name = None):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.length = length
        self.lanes = [Lane(i,length) for i in range(lanes)]
        self.speed_limit = speed_limit
        self.name = name

        #setting lanes to have its neibhor lane(i.e left/rigth)
        for i in range(lanes):
            left  = self.lanes[i-1] if i > 0 else None
            right = self.lanes[i+1] if i < lanes - 1 else None
            self.lanes[i].set_neighbors(left,right)

    def get_lane(self, index):
        if 0 <= index < len(self.lanes):
            return self.lanes[index]
        return None
