class Snake:

    _cor = []

    def __init__(self, head):
        self._head = head
        self._cor = [self._head]
        self._size = len(self._cor)
        self._direction = None


    def snakeMaker(self):
        if self._direction == 0:
            self._cor.append((self._cor[-1][0], self._cor[-1][1] + 1))
        elif self._direction == 1:
            self._cor.append((self._cor[-1][0] - 1, self._cor[-1][1]))
        elif self._direction == 2:
            self._cor.append((self._cor[-1][0], self._cor[-1][1] - 1))
        elif self._direction == 3:
            self._cor.append((self._cor[-1][0] + 1, self._cor[-1][1])) 


    def move(self):
        if self._direction == 0:
            future_head = (self._head[0], self._head[1] - 1)
            self._cor.insert(0, future_head)
            del self._cor[-1]
            self._head = self._cor[0]

        elif self._direction == 1:
            future_head = (self._head[0] + 1, self._head[1])
            self._cor.insert(0, future_head)
            del self._cor[-1]
            self._head = self._cor[0]

        elif self._direction == 2:
            future_head = (self._head[0], self._head[1] + 1)
            self._cor.insert(0, future_head)
            del self._cor[-1]
            self._head = self._cor[0]

        elif self._direction == 3:
            future_head = (self._head[0] - 1, self._head[1])
            self._cor.insert(0, future_head)
            del self._cor[-1]
            self._head = self._cor[0]