# def get_id_by_uuid(uuid,Model):
#     try:
#         id = Model.objects.filter(uuid=uuid,is_delete=False).first().v
#     except Exception as e:
#         return {"error": str(e)}
