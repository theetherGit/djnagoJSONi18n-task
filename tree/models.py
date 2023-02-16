from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class TreeNode(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_descendant_count()}"
