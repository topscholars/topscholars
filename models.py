# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.db import connection
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Selectiongroup(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    groupname = models.CharField(max_length=100L, db_column='GroupName') # Field name made lowercase.
    system = models.IntegerField(db_column='System') # Field name made lowercase.
    entityid = models.IntegerField(db_column='EntityId') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'selectiongroup'

class Selectionlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    selectiongroupid = models.IntegerField(db_column='SelectionGroupId') # Field name made lowercase.
    selectionname = models.CharField(max_length=100L, db_column='SelectionName') # Field name made lowercase.
    selectionvalue = models.CharField(max_length=100L, db_column='SelectionValue') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    class Meta:
        db_table = 'selectionlist'

class Userlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    firstname = models.CharField(max_length=50L, db_column='FirstName') # Field name made lowercase.
    lastname = models.CharField(max_length=50L, db_column='LastName') # Field name made lowercase.
    middlename = models.CharField(max_length=50L, db_column='MiddleName', blank=True) # Field name made lowercase.
    salutation = models.IntegerField(db_column='Salutation') # Field name made lowercase.
    title = models.CharField(max_length=100L, db_column='Title', blank=True) # Field name made lowercase.
    department = models.CharField(max_length=100L, db_column='Department', blank=True) # Field name made lowercase.
    dob = models.DateField(db_column='DOB') # Field name made lowercase.
    homephone = models.CharField(max_length=25L, db_column='HomePhone', blank=True) # Field name made lowercase.
    officephone = models.CharField(max_length=25L, db_column='OfficePhone', blank=True) # Field name made lowercase.
    officeext = models.CharField(max_length=5L, db_column='OfficeExt', blank=True) # Field name made lowercase.
    mobilephone = models.CharField(max_length=25L, db_column='MobilePhone', blank=True) # Field name made lowercase.
    emailaddress = models.CharField(max_length=100L, db_column='EmailAddress', blank=True) # Field name made lowercase.
    securityprofileid = models.IntegerField(db_column='SecurityProfileId') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    
    class Meta:
        db_table = 'userlist'

class Rubric(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    entityid = models.IntegerField(db_column='EntityId') # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True) # Field name made lowercase.
    typeid = models.ForeignKey(Selectionlist,related_name="Rubrictoselectionlist",db_column='TypeId') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'rubric'

class Assignment(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True) # Field name made lowercase.
    minwords = models.IntegerField(db_column='MinWords') # Field name made lowercase.
    maxwords = models.IntegerField(db_column='MaxWords') # Field name made lowercase.
    rubricid = models.ForeignKey(Rubric,related_name="Assignmenttorubric",db_column='RubricId') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'assignment'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class Classlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    courseid = models.IntegerField(db_column='CourseId') # Field name made lowercase.
    classname = models.CharField(max_length=100L, db_column='ClassName') # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True) # Field name made lowercase.
    rubricid = models.ForeignKey(Rubric,db_column='RubricId') # Field name made lowercase.
    paxmin = models.IntegerField(db_column='PaxMin') # Field name made lowercase.
    paxmax = models.IntegerField(db_column='PaxMax') # Field name made lowercase.
    prerequired = models.IntegerField(db_column='PreRequired') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'classlist'

class Classschedule(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    classid = models.ForeignKey(Classlist,db_column='ClassId') # Field name made lowercase.
    code = models.CharField(max_length=50L, db_column='Code', blank=True) # Field name made lowercase.
    subcode = models.CharField(max_length=50L, db_column='SubCode', blank=True) # Field name made lowercase.
    teacherid = models.IntegerField(db_column='TeacherId') # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate') # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate') # Field name made lowercase.
    starttime = models.CharField(max_length=5L, db_column='StartTime', blank=True) # Field name made lowercase.
    endtime = models.CharField(max_length=5L, db_column='EndTime', blank=True) # Field name made lowercase.
    dayofweek = models.CharField(max_length=30L, db_column='DayOfWeek', blank=True) # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    def getNumberOfStudents(self):
        return Studentclass.objects.filter(classscheduleid = self.id).count()
    class Meta:
        db_table = 'classschedule'

class Clientlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    registeredname = models.CharField(max_length=100L, db_column='RegisteredName', blank=True) # Field name made lowercase.
    shortname = models.CharField(max_length=100L, db_column='ShortName', blank=True) # Field name made lowercase.
    recordtype = models.IntegerField(db_column='RecordType') # Field name made lowercase.
    address1 = models.CharField(max_length=100L, db_column='Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=100L, db_column='Address2', blank=True) # Field name made lowercase.
    address3 = models.CharField(max_length=100L, db_column='Address3', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=50L, db_column='City', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=50L, db_column='State', blank=True) # Field name made lowercase.
    zipcode = models.CharField(max_length=15L, db_column='ZipCode', blank=True) # Field name made lowercase.
    country = models.CharField(max_length=50L, db_column='Country', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=100L, db_column='Website', blank=True) # Field name made lowercase.
    emailaddress = models.CharField(max_length=100L, db_column='EmailAddress', blank=True) # Field name made lowercase.
    phone1 = models.CharField(max_length=25L, db_column='Phone1', blank=True) # Field name made lowercase.
    phone2 = models.CharField(max_length=25L, db_column='Phone2', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=25L, db_column='Fax', blank=True) # Field name made lowercase.
    contact_name = models.CharField(max_length=100L, db_column='Contact_Name', blank=True) # Field name made lowercase.
    contact_salutation = models.IntegerField(db_column='Contact_Salutation') # Field name made lowercase.
    contact_title = models.CharField(max_length=100L, db_column='Contact_Title', blank=True) # Field name made lowercase.
    contact_email = models.CharField(max_length=100L, db_column='Contact_Email', blank=True) # Field name made lowercase.
    contact_phone = models.CharField(max_length=25L, db_column='Contact_Phone', blank=True) # Field name made lowercase.
    contact_ext = models.CharField(max_length=5L, db_column='Contact_Ext', blank=True) # Field name made lowercase.
    contact_mobile = models.CharField(max_length=25L, db_column='Contact_Mobile', blank=True) # Field name made lowercase.
    timezone = models.IntegerField(db_column='TimeZone') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    class Meta:
        db_table = 'clientlist'

class Course(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True) # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'course'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class Entity(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    mainentity = models.IntegerField(db_column='MainEntity') # Field name made lowercase.
    class Meta:
        db_table = 'entity'

class Leadlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    firstname = models.CharField(max_length=50L, db_column='FirstName', blank=True) # Field name made lowercase.
    lastname = models.CharField(max_length=50L, db_column='LastName', blank=True) # Field name made lowercase.
    middlename = models.CharField(max_length=50L, db_column='MiddleName', blank=True) # Field name made lowercase.
    interest = models.TextField(db_column='Interest', blank=True) # Field name made lowercase.
    description = models.TextField(db_column='Description') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'leadlist'

class License(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    key = models.CharField(max_length=255L, db_column='Key') # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId') # Field name made lowercase.
    type = models.IntegerField(db_column='Type') # Field name made lowercase.
    expirationdt = models.DateTimeField(db_column='ExpirationDT') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'license'

class Login(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    loginname = models.CharField(max_length=50L, db_column='LoginName') # Field name made lowercase.
    password = models.CharField(max_length=100L, db_column='Password') # Field name made lowercase.
    hint = models.CharField(max_length=100L, db_column='Hint', blank=True) # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='UserTypeId') # Field name made lowercase.
    recid = models.IntegerField(db_column='RecId') # Field name made lowercase.
    status = models.CharField(max_length=25L, db_column='Status', blank=True) # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'login'

class Module(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    class Meta:
        db_table = 'module'

class Rubriccriteria(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    rubricid = models.IntegerField(db_column='RubricId') # Field name made lowercase.
    criteria = models.CharField(max_length=100L, db_column='Criteria') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'rubriccriteria'

class Rubricscale(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    rubricid = models.IntegerField(db_column='RubricId') # Field name made lowercase.
    scale = models.CharField(max_length=100L, db_column='Scale') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    order = models.IntegerField(db_column='Order') # Field name made lowercase.
    class Meta:
        db_table = 'rubricscale'

class Rubriclink(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    entityid = models.ForeignKey(Entity,related_name="Rubriclinktoentity", db_column='EntityId') # Field name made lowercase.
    recid = models.IntegerField(db_column='RecId') # Field name made lowercase.
    rubiccriteriaid = models.ForeignKey(Rubriccriteria,related_name="Rubriclinktorubriccriteria",db_column='RubicCriteriaId') # Field name made lowercase.
    rubricscaleid = models.ForeignKey(Rubricscale,related_name="Rubriclinktorubricscale",db_column='RubricScaleId') # Field name made lowercase.
    class Meta:
        db_table = 'rubriclink'

class Security(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    securityprofileid = models.IntegerField(db_column='SecurityProfileId') # Field name made lowercase.
    entityid = models.IntegerField(db_column='EntityId') # Field name made lowercase.
    view = models.IntegerField(db_column='View') # Field name made lowercase.
    create = models.IntegerField(db_column='Create') # Field name made lowercase.
    edit = models.IntegerField(db_column='Edit') # Field name made lowercase.
    delete = models.IntegerField(db_column='Delete') # Field name made lowercase.
    class Meta:
        db_table = 'security'

class Securityprofile(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'securityprofile'

class Studentlist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    firstname = models.CharField(max_length=50L, db_column='FirstName') # Field name made lowercase.
    lastname = models.CharField(max_length=50L, db_column='LastName') # Field name made lowercase.
    middlename = models.CharField(max_length=50L, db_column='MiddleName', blank=True) # Field name made lowercase.
    address1 = models.CharField(max_length=100L, db_column='Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=100L, db_column='Address2', blank=True) # Field name made lowercase.
    address3 = models.CharField(max_length=100L, db_column='Address3', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=50L, db_column='City', blank=True) # Field name made lowercase.
    zipcode = models.CharField(max_length=15L, db_column='ZipCode', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=50L, db_column='State', blank=True) # Field name made lowercase.
    country = models.CharField(max_length=50L, db_column='Country', blank=True) # Field name made lowercase.
    timezone = models.IntegerField(db_column='TimeZone') # Field name made lowercase.
    mobilephone = models.CharField(max_length=25L, db_column='MobilePhone', blank=True) # Field name made lowercase.
    homephone = models.CharField(max_length=25L, db_column='HomePhone', blank=True) # Field name made lowercase.
    otherphone = models.CharField(max_length=25L, db_column='OtherPhone', blank=True) # Field name made lowercase.
    otherphonetype = models.IntegerField(db_column='OtherPhoneType') # Field name made lowercase.
    emailaddress1 = models.CharField(max_length=100L, db_column='EmailAddress1', blank=True) # Field name made lowercase.
    emailaddress2 = models.CharField(max_length=100L, db_column='EmailAddress2', blank=True) # Field name made lowercase.
    dob = models.DateField(db_column='DOB') # Field name made lowercase.
    gender = models.IntegerField(db_column='Gender') # Field name made lowercase.
    salutation = models.IntegerField(db_column='Salutation') # Field name made lowercase.
    currentaccademicyear = models.IntegerField(db_column='CurrentAccademicYear') # Field name made lowercase.
    enrollmentdt = models.DateField(db_column='EnrollmentDT') # Field name made lowercase.
    leadid = models.IntegerField(db_column='LeadId') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    
    def getFullName(self):
        fullname = ''
        if self.middlename is not None:
            fullname = self.firstname + ' ' + self.middlename + ' ' + self.lastname
        else:
            fullname = self.firstname + ' ' + self.lastname
        return fullname

    def getNextAssginmentDate(self):
        stdid=self.id
        cursor = connection.cursor()
        cursor.execute('select min(duedate) from submission where progress <> 100 and studentid=%s',[stdid])
        row = cursor.fetchone()
        return row[0]

    def getStudentGrade(self):
        stdid=self.id
        cursor = connection.cursor()
        cursor.execute('select grade from Studentclass where studentid = %s and createddt = (select max(createddt) from Studentclass where studentid = %s)',[stdid,stdid])
        row = cursor.fetchone()
        return row[0]
    
    def getStudentPreviousClass(self):
        stdid=self.id
        cursor = connection.cursor()
        cursor.execute('select cs.code from studentlist as st join studentclass as sc on st.id = sc.studentid join classschedule as cs on sc.classscheduleid = cs.id where st.id = %s and cs.startdate = (select max(cs.startdate) from studentclass as sc join classschedule as cs on sc.classscheduleid = cs.id where sc.studentid = %s )',[stdid,stdid])
        row = cursor.fetchone()
        return row[0]
    
    def getStudentCurrentClass(self):
        stdid=self.id
        cursor = connection.cursor()
        cursor.execute('select cs.code from studentlist as st join studentclass as sc on st.id = sc.studentid join classschedule as cs on sc.classscheduleid = cs.id where st.id = %s and cs.createddt = (select max(cs.createddt) from studentclass as sc join classschedule as cs on sc.classscheduleid = cs.id where sc.studentid = %s )',[stdid,stdid])
        row = cursor.fetchone()
        return row[0]
    
    class Meta:
        db_table = 'studentlist'

class Studentclass(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    studentid = models.ForeignKey(Studentlist,related_name="Studentclasstostudents",db_column='StudentId') # Field name made lowercase.
    classscheduleid = models.ForeignKey(Classschedule,related_name="Studentclasstoclasses",db_column='ClassScheduleId') # Field name made lowercase.
    grade = models.IntegerField(db_column='Grade') # Field name made lowercase.
    status = models.IntegerField(db_column='Status') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'studentclass'

class Submission(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    studentid = models.ForeignKey(Studentlist,related_name="Submissiontostudents",db_column='StudentId') # Field name made lowercase.
    teacherid = models.ForeignKey(Userlist,related_name="Submissiontouserlist",db_column='TeacherId') # Field name made lowercase.
    assignmentid = models.ForeignKey(Assignment,related_name="Submissiontoassignment",db_column='AssignmentId') # Field name made lowercase.
    duedate = models.DateField(db_column='DueDate') # Field name made lowercase.
    progress = models.IntegerField(db_column='Progress') # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True) # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.

    def getLatestVersion(self):
        submissionid=self.id
        cursor = connection.cursor()
        cursor.execute('select version from Submissionversion where submissionid = %s and version = (select max(version) from Submissionversion where submissionid = %s and deleted = 0)',[submissionid,submissionid])
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return 0
    
    class Meta:
        unique_together = (('studentid', 'teacherid', 'assignmentid'),)
        db_table = 'submission'

class Submissionversion(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    submissionid = models.ForeignKey(Submission,related_name="Submissionversiontosubmission",db_column='SubMissionId') # Field name made lowercase.
    version = models.IntegerField(db_column='Version') # Field name made lowercase.
    essay = models.TextField(db_column='Essay', blank=True) # Field name made lowercase.
    studentstatus = models.IntegerField(db_column='StudentStatus') # Field name made lowercase.
    teacherstatus = models.IntegerField(db_column='TeacherStatus') # Field name made lowercase.
    stage = models.IntegerField(db_column='Stage') # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True) # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    class Meta:
        db_table = 'submissionversion'

class Submissionversionhighlight(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    submissionversionid = models.IntegerField(db_column='SubmissionVersionId') # Field name made lowercase.
    startposition = models.IntegerField(db_column='StartPosition') # Field name made lowercase.
    hightlighttext = models.TextField(db_column='HightlightText') # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True) # Field name made lowercase.
    weight = models.IntegerField(db_column='Weight') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    class Meta:
        db_table = 'submissionversionhighlight'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId') # Field name made lowercase.
    category = models.IntegerField(db_column='Category') # Field name made lowercase.
    subcategory = models.IntegerField(db_column='SubCategory') # Field name made lowercase.
    tagcolor = models.CharField(max_length=7L,db_column='TagColor') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    system = models.IntegerField(db_column='System') # Field name made lowercase.
    class Meta:
        db_table = 'tag'

class Tagcategory(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'tagcategory'

class Taglink(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    entityid = models.ForeignKey(Entity,related_name="Taglinktoentity", db_column='EntityId') # Field name made lowercase.
    recid = models.IntegerField(db_column='RecId') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    tagid = models.ForeignKey(Tag,related_name="Taglinktotag",db_column='TagId') # Field name made lowercase.
    class Meta:
        db_table = 'taglink'

class Taglocallize(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    tagid = models.IntegerField(db_column='TagId') # Field name made lowercase.
    taglocalname = models.CharField(max_length=100L, db_column='TagLocalName') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'taglocallize'

class Tagsubcategory(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryId') # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name') # Field name made lowercase.
    createddt = models.DateTimeField(db_column='CreatedDT') # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy') # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT') # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy') # Field name made lowercase.
    disabled = models.IntegerField(db_column='Disabled') # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted') # Field name made lowercase.
    clientid = models.IntegerField(db_column='ClientId') # Field name made lowercase.
    class Meta:
        db_table = 'tagsubcategory'

class Usertype(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    type = models.CharField(max_length=50L, db_column='Type') # Field name made lowercase.
    class Meta:
        db_table = 'usertype'

class Classassignment(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    classid = models.ForeignKey(Classschedule,related_name="Classassignmenttoclassschedule", db_column='ClassId') # Field name made lowercase.
    assignmentid = models.ForeignKey(Assignment,related_name="Classassignmenttoassignment", db_column='AssignmentId') # Field name made lowercase.
    class Meta:
        db_table = 'classassignment'

class TagEntity(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    tagid = models.ForeignKey(Tag,related_name="Tagentitytotag", db_column='TagId') # Field name made lowercase.
    entityid = models.ForeignKey(Entity,related_name="Tagentitytoentity", db_column='EntityId') # Field name made lowercase.
    class Meta:
        db_table = 'TagEntity'

