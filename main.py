#DEBUG = True
if 'DEBUG' in globals():
    def dprint(*objects, sep=' ', end='\n'):
        print(*objects, sep=sep, end=end)
else:
    def dprint(*objects, sep=' ', end='\n'):
        pass
