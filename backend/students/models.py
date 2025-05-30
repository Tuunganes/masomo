from django.db import models
from django.utils.text import slugify

class Student(models.Model):
    STATUS_CHOICES = [
        ('active',     'Active'),
        ('alumni',     'Alumni'),
        ('transferred','Transferred'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        
    ]

    CLASS_LEVEL_CHOICES = [
        # Maternelle
        ('m1',  '1ère maternelle'),
        ('m2',  '2ème maternelle'),
        ('m3',  '3ème maternelle'),
        # Primaire
        ('p1',  '1ère primaire'),
        ('p2',  '2ème primaire'),
        ('p3',  '3ème primaire'),
        ('p4',  '4ème primaire'),
        ('p5',  '5ème primaire'),
        ('p6',  '6ème primaire'),
        ('p7',  '7ème primaire'),
        ('p8',  '8ème primaire'),
        # Secondaire
        ('s1',  '1ère secondaire'),
        ('s2',  '2ème secondaire'),
        ('s3',  '3ème secondaire'),
        ('s4',  '4ème secondaire'),
    ]

    # … existing fields …
    class_level   = models.CharField(
        max_length=3,
        choices=CLASS_LEVEL_CHOICES,
        blank=True
    )

    student_id       = models.CharField(max_length=30, unique=True)
    first_name       = models.CharField(max_length=100)
    last_name        = models.CharField(max_length=100)
    gender           = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth    = models.DateField()
    nationality      = models.CharField(max_length=100, blank=True)
    address          = models.CharField(max_length=255, blank=True)
    phone            = models.CharField(max_length=30, blank=True)
    email            = models.EmailField(blank=True)
    guardian_name    = models.CharField(max_length=120, blank=True)
    guardian_phone   = models.CharField(max_length=30, blank=True)
    #class_level      = models.CharField(max_length=50, blank=True)
    enrol_date       = models.DateField()
    status           = models.CharField(max_length=12, choices=STATUS_CHOICES, default='active')
    photo            = models.ImageField(upload_to='student_photos/', blank=True)

    slug             = models.SlugField(unique=True, blank=True)
    registration_date= models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.first_name}-{self.last_name}-somo")
            unique = base
            cnt = 1
            while Student.objects.filter(slug=unique).exists():
                unique = f"{base}-{cnt}"
                cnt += 1
            self.slug = unique
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
