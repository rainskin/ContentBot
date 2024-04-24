from aiogram import types


def get_marker(msg: types.Message):

    if msg.media_group_id:
        pass
    if msg.text:
        marker = msg.text
    elif msg.photo:
        marker = msg.photo[0].file_unique_id
    elif msg.video:
        marker = msg.video.file_unique_id
    elif msg.sticker:
        marker = msg.sticker.file_unique_id
    elif msg.voice:
        marker = msg.voice.file_unique_id
    elif msg.poll:
        marker = msg.poll.question
    elif msg.video_note:
        marker = msg.video_note.file_unique_id
    elif msg.audio:
        marker = msg.audio.file_unique_id
    elif msg.document:
        marker = msg.document.file_unique_id
    else:
        marker = None

    return marker
