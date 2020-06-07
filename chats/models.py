# from django.db import models
#
# from accounting.models import CustomUser
# from classrooms.models import Classroom
#
#
# class Chat(models.Model):
#     pass
#
#
# class ClassroomChat(Chat):
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="chat")
#
#
# class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
#     text = models.TextField()
#     sender = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
