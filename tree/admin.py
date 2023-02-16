from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from tree.models import TreeNode

admin.site.register(TreeNode, MPTTModelAdmin)
