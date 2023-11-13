# command dict form
# example: !search <title or http address>

class Commands:
    cmds = dict()
    prefix = "!"
    def __init__(self, pre):
        self.prefix = pre
        self.cmds["{}{}".format(self.prefix, "delete")] = self.delete
        self.cmds["{}{}".format(self.prefix, "search")] = self.search
        self.cmds["{}{}".format(self.prefix, "검색")] = self.search

    def cmd(self, command):
        if (command in self.cmds):
            return True
        else:
            return False

    def delete(self, content, params = None):
        if (self.cmd(content) == True):
            return True
        else:
            return False

    def search(self, content):
        try:
            command, keyword = content.split(" ", 1)
            if (self.cmd(command) == True):
                return keyword
            else:
                return False
        except:
            return False
