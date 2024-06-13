from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    mobilenumber = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username

class TransportRequest(models.Model):
    requester_id = models.ForeignKey(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()
    receiver_mobilenumber = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField()
    asset_type = models.CharField(max_length=20)
    sensitivity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='unapplied')

    def __str__(self):
        return f"Request from {self.from_location} to {self.to_location} on {self.date} from requester_id: {self.requester_id}"

class Ride(models.Model):
    rider_id = models.ForeignKey(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    medium = models.CharField(max_length=10, default='train')

    def __str__(self):
        return f"Ride  from {self.from_location} to {self.to_location} on {self.date} by rider_id: {self.rider_id}"

class ReqApplication(models.Model):
    request_id = models.ForeignKey(TransportRequest, on_delete=models.CASCADE, to_field='id')
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE, to_field='id')
    status = models.CharField(max_length=10)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"request  from {self.request_id.id} to {self.ride_id.id} on {self.datetime} by status: {self.status}"