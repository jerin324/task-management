from .models import BoardMember


def is_board_member(board, user):

    if board.owner == user:
        return True

    return BoardMember.objects.filter(
        board=board,
        user=user
    ).exists()