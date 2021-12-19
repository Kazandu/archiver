import rclone_move

def executePostexec(FinalFile,logWriter,dldir):
    rclone_move.rclonemove(FinalFile,logWriter,dldir)