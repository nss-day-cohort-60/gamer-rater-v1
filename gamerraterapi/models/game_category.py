from django.db import models

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    # I do not include _id at the end of the foreign keys because
    # Django will automatically add _id at the end of the column name
    # for me.  If I do it, the column name would be, for example,
    # category_id_id
