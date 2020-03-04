from django.db import models
import random,os

# Create your models here.
def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance,filename):
    new_filename =  random.randint(1,32514146)
    name, ext = get_file_ext(filename)
    final_name = f'{new_filename}{ext}'
    return "products/{new_filename}/{final_name}".format(new_filename=new_filename,
                                                         final_name=final_name)
class Upload(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

