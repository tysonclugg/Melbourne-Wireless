# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

#from django.db import models
from django.contrib.gis.db import models

from localflavor.au.au_states import STATE_CHOICES
from localflavor.au.forms import AUPostCodeField, AUPhoneNumberField

from django.contrib.auth import models as auth
from django.core.urlresolvers import reverse
import hashlib

CARD_STATUS_CHOICES = (
    (0, 'Card not required'),
    (1, 'Card dispatched'),
    (2, 'Card to be mailed'),
    (3, 'Card to be picked up from meeting'),
)

class Member(models.Model):
    id = models.AutoField(primary_key=True, db_column='memberNo')
    first_name = models.CharField(max_length=60, db_column='firstName')
    last_name = models.CharField(max_length=120, db_column='surName')
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    suburb = models.CharField(max_length=90)
    state = models.CharField(max_length=9, choices=STATE_CHOICES)
    postcode = models.CharField(max_length=18)
    email = models.EmailField(max_length=150)
    occupation = models.CharField(max_length=90)
    dob = models.DateField()
    skills = models.TextField()
    heard = models.TextField()
    expect = models.TextField()
    nice = models.TextField()
    member_of = models.TextField(db_column='memberOf')
    spend = models.CharField(max_length=60)
    applied = models.DateField(db_column='appliedDate')
    approved = models.DateField(db_column='approvedDate')
    comments = models.TextField()
    membership_card = models.IntegerField(db_column='cardStatus', choices=CARD_STATUS_CHOICES)
    def __unicode__(self):
        return u'%d: %s, %s' % (self.id, self.last_name, self.first_name)
    def get_absolute_url(self):
        return 'http://www.melbournewireless.org.au/committee/members/view?%d' % self.id
    class Meta:
        db_table = u'members'
        ordering = ['id']

class Receipt(models.Model):
    id = models.AutoField(primary_key=True, db_column='receiptId')
    to = models.CharField(max_length=120)
    email = models.EmailField(max_length=225)
    sent = models.DateField(db_column='receiptDate')
    def __unicode__(self):
        return u'%s: %s <%s>' % (self.sent, self.to, self.email)
    class Meta:
        db_table = u'receiptHead'
        ordering = ['-id']

class ReceiptLine(Receipt):
    receipt = models.OneToOneField('Receipt', db_column='receiptid', parent_link=True)
    description = models.CharField(max_length=225, db_column='for')
    amount = models.FloatField()
    def __unicode__(self):
        return u'%s: %s: $%2.2f' % (self.receipt, self.description, self.amount)
    class Meta:
        db_table = u'receiptLine'
        ordering = ['receipt']

class MemberPayment(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', db_column='memberNo') # Field name made lowercase.
    start_date = models.DateField(db_column='startDate') # Field name made lowercase.
    end_date = models.DateField(db_column='endDate') # Field name made lowercase.
    paid = models.BooleanField()
    card = models.BooleanField()
    receipt = models.ForeignKey('Receipt', db_column='receiptNo') # Field name made lowercase.
    def __unicode__(self):
        return u'%s to %s, receipt #%d (%s)' % (self.start_date, self.end_date, self.receipt_id, self.member)
    class Meta:
        db_table = u'membersYears'
        ordering = ['id']

class UserManager(models.Manager):
    def authenticate(self, username=None, password=None):
        # Always validate user supplied inputs!
        if 1 > len(username) > 10 \
        or 1 > len(password) > 100:
            return None
        hash = hashlib.md5(password)
        try:
            mw_user = User.objects.get(
                pk = username,
                password = hash.hexdigest(),
            )
            try:
                return auth.User.objects.get(pk=username)
            except auth.User.DoesNotExist:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return auth.User.objects.get(pk=user_id)
        except auth.User.DoesNotExist:
            return None


class User(models.Model):
    id = models.CharField(max_length=30, primary_key=True, db_column='username')
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=96)
    email_confirmed = models.BooleanField(db_column='confirm')
    membership = models.ForeignKey('Member', db_column='memberNo', blank=True, null=True) # Field name made lowercase.
    theme = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=765)
    phone = models.CharField(max_length=45)
    last_ip = models.CharField(max_length=48)
    last_seen = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.IntegerField(db_column='failedAttempts') # Field name made lowercase.
    registered = models.DateField(db_column='registeredDate') # Field name made lowercase.
    unconfirmed_email = models.EmailField(max_length=150, blank=True, db_column='email_unconfirmed')
    subscribed = models.IntegerField(null=True, blank=True)
    adv = models.IntegerField(null=True, blank=True)
    objects = UserManager()
    def __unicode__(self):
        return u'%s' % self.id
    def get_absolute_url(self):
        return 'http://www.melbournewireless.org.au/users/?%s' % self.id
    class Meta:
        db_table = u'users'
        ordering = ['id']

"""
class Group(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    users = models.ManyToManyField('User', through='GroupMember')

class GroupManager(models.Manager):
    def get_query_set(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''
            SELECT CONCAT(groupname,':',username) as id, groupname, username FROM groups
        ''')
        return super(GroupManager, self).get_query_set().extra


class GroupMember(models.Model):
    group = models.ForeignKey('auth.Group', db_column='groupname', to_field='name')
    user = models.ForeignKey('User', db_column='username')
    class Meta:
        db_table = u'groups'
        ordering = ['group', 'user']
"""


class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    min_lat = models.FloatField(db_column='minLat')
    max_lat = models.FloatField(db_column='maxLat')
    min_long = models.FloatField(db_column='minLong')
    max_long = models.FloatField(db_column='maxLong')
    mailing_list = models.CharField(max_length=300, db_column='mailingList')
    description = models.TextField()
    wiki = models.TextField(blank=True, db_column='wikiurl')
    newsgroup = models.CharField(max_length=450, blank=True)
    def __unicode__(self):
        return u'%s' % self.name
    def get_absolute_url(self):
        return 'http://www.melbournewireless.org.au/maps/area?id=%d' % self.id
    class Meta:
        db_table = u'areas'
        ordering = ['name']

class Committee(Member):
    member = models.OneToOneField('Member', db_column='memberNo', parent_link=True)
    position = models.CharField(max_length=75, db_column='Position')
    year_ending = models.IntegerField(db_column='yearEnding')
    def __unicode__(self):
        return u'%s: %s - %s' % (self.year_ending, self.position, self.member)
    class Meta:
        db_table = u'committee'
        ordering = ['-year_ending', 'position']

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    when = models.DateTimeField()
    who = models.CharField(max_length=96)
    what = models.CharField(max_length=765)
    ip = models.CharField(max_length=48, blank=True)
    def __unicode__(self):
        return u'%s: %s (%s)' % (self.when, self.what, self.who)
    class Meta:
        db_table = u'log'

class Menu(models.Model):
    id = models.CharField(max_length=30, db_column='menuID', primary_key=True) # Field name made lowercase.
    parent = models.ForeignKey('self', max_length=30, db_column='parentID') # Field name made lowercase.
    text = models.CharField(max_length=75, db_column='menuText') # Field name made lowercase.
    url = models.CharField(max_length=300, db_column='menuURL') # Field name made lowercase.
    zorder = models.IntegerField(db_column='zOrder') # Field name made lowercase.
    group_name = models.CharField(max_length=48, db_column='groupname')
    def __unicode__(self):
        return u'%s' % self.url
    def get_absolute_url(self):
        return '/%s' % self.url
        return 'http://www.melbournewireless.org.au/%s' % self.url
    class Meta:
        db_table = u'menu'

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=300)
    story = models.TextField()
    posted = models.DateTimeField(db_column='date')
    def __unicode__(self):
        return u'%s: %s' % (self.posted, self.headline)
    def get_absolute_url(self):
        return 'http://www.melbournewireless.org.au/news?id=%d' % self.id
    class Meta:
        db_table = u'news'

NODE_STATUS_INTERESTED = 'interested'
NODE_STATUS_GATHERING = 'gathering'
NODE_STATUS_BUILDING = 'building'
NODE_STATUS_TESTING = 'testing'
NODE_STATUS_OPERATIONAL = 'operational'

NODE_STATUS_CHOICES = (
    # ordering must be from lowest to highest
    (NODE_STATUS_INTERESTED, 'Interested'),
    (NODE_STATUS_GATHERING, 'Gathering'),
    (NODE_STATUS_BUILDING, 'Building'),
    (NODE_STATUS_TESTING, 'Testing'),
    (NODE_STATUS_OPERATIONAL, 'Operational'),
)

NODE_STATUS_COLORS = {
    NODE_STATUS_INTERESTED: 'darkred',
    NODE_STATUS_GATHERING: 'red',
    NODE_STATUS_BUILDING: 'orange',
    NODE_STATUS_TESTING: '#1E90FF',
    NODE_STATUS_OPERATIONAL: 'green',
}

class Node(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=90)
    owner = models.ForeignKey('User', db_column='owner')
    suburb = models.CharField(max_length=90)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(null=True, blank=True)
    url = models.CharField(max_length=180)
    area = models.ForeignKey('Area', blank=True, db_column='area')
    status = models.CharField(max_length=36, choices=NODE_STATUS_CHOICES)
    updated = models.DateTimeField()
    old_password = models.CharField(max_length=120, db_column='oldPassword')
    old_email = models.EmailField(max_length=180, db_column='oldEmail')
    notification_distance = models.IntegerField(null=True, blank=True, db_column='optdist')
    def __unicode__(self):
        return u'%s: %s - %s (%s)' % (self.id, self.name, self.suburb, self.owner_id)
    def get_absolute_url(self):
        return '/maps/node/{0}/'.format(self.id.upper())
        return reverse('maps_node_view', args=[self.id])
    class Meta:
        db_table = u'nodes'
        ordering = ['id']

    # shorthand property names
    lat = property(lambda self: self.latitude)
    lng = property(lambda self: self.longitude)
    alt = property(lambda self: self.altitude)

    @property
    def links(self):
        '''Returns queryset of all links related to this node'''
        return Link.objects.filter(
            models.Q(
                interface_1__node = self,
            ) | models.Q(
                interface_2__node = self,
            )
        )

    @property
    def other_links(self):
        '''Returns queryset of all links NOT related to this node'''
        return Link.objects.exclude(
            models.Q(
                interface_1__node = self,
            ) | models.Q(
                interface_2__node = self,
            )
        )

class NodeScore(models.Model):
    node = models.OneToOneField('Node', primary_key=True, db_column='node')
    user = models.ForeignKey('User', db_column='username')
    area = models.ForeignKey('Area', db_column='area')
    interfaces = models.IntegerField()
    links = models.IntegerField()
    distance = models.FloatField()
    services = models.IntegerField()
    updated = models.DateTimeField()
    score = models.FloatField()
    def __unicode__(self):
        return u'%2.2f: %s' % (self.score, self.node)
    class Meta:
        db_table = u'node_score'
        ordering = ['-score', 'node']

class NodeHost(models.Model):
    address = models.CharField(max_length=45, primary_key=True)
    node = models.ForeignKey('Node', db_column='node_id')
    host = models.CharField(max_length=384)
    def __unicode__(self):
        return u'%s %s %s' % (self.address, self.host, self.node)
    class Meta:
        db_table = u'nodes_hosts'
        ordering = ['address', 'host', 'node']

INTERFACE_MODE_UNKNOWN = 'unkn'
INTERFACE_MODE_PACKET = 'pckt'
INTERFACE_MODE_FHSS = 'fhss'
INTERFACE_MODE_802_11b_BSS = 'bss'
INTERFACE_MODE_802_11b_IBSS = 'ibss'
INTERFACE_MODE_802_11g_BSS = 'bssg'
INTERFACE_MODE_802_11g_IBSS = 'ibsg'
INTERFACE_MODE_802_11bg_BSS = 'gbss'
INTERFACE_MODE_802_11bg_IBSS = 'gibs'
INTERFACE_MODE_802_11a_BSS = 'gjbs'
INTERFACE_MODE_802_11a_IBSS = 'gkbs'
INTERFACE_MODE_VENDOR = 'vend'
INTERFACE_MODE_VENDOR58 = 'vind'
INTERFACE_MODE_VIRTUAL = 'virt'

INTERFACE_MODE_CHOICES = (
    (INTERFACE_MODE_UNKNOWN, 'Unknown'),
    (INTERFACE_MODE_PACKET, 'Packet radio'),
    (INTERFACE_MODE_FHSS, '802.11 FHSS'),
    (INTERFACE_MODE_802_11b_BSS, '802.11b BSS (Infrastructure)'),
    (INTERFACE_MODE_802_11b_IBSS, '802.11b IBSS (Ad-hoc)'),
    (INTERFACE_MODE_802_11g_BSS, '802.11g BSS (Infrastructure)'),
    (INTERFACE_MODE_802_11g_IBSS, '802.11g IBSS (Ad-hoc)'),
    (INTERFACE_MODE_802_11bg_BSS, '802.11b/g BSS (Infrastructure)'),
    (INTERFACE_MODE_802_11bg_IBSS, '802.11b/g IBSS (Ad-hoc)'),
    (INTERFACE_MODE_802_11a_BSS, '802.11a BSS (Infrastructure)'),
    (INTERFACE_MODE_802_11a_IBSS, '802.11a IBSS (Ad-hoc)'),
    (INTERFACE_MODE_VENDOR, 'Vendor/proprietry 2.4Ghz'),
    (INTERFACE_MODE_VENDOR58, 'Vendor/proprietry 5.8Ghz'),
    (INTERFACE_MODE_VIRTUAL, 'Virtual'),
)

NODE_CLASS_UNKNOWN = 'unknown'
NODE_CLASS_ADHOC = 'adhoc'
NODE_CLASS_P2P = 'p2p'
NODE_CLASS_P2MP = 'p2mp'
NODE_CLASS_CLIENT = 'client'

NODE_CLASS_CHOICES = (
    (NODE_CLASS_UNKNOWN, 'Unknown'),
    (NODE_CLASS_ADHOC, 'Ad-hoc'),
    (NODE_CLASS_P2P, 'Point to Point'),
    (NODE_CLASS_P2MP, 'Point to Multipoint'),
    (NODE_CLASS_CLIENT, 'Client'),
)

class Interface(models.Model):
    id = models.AutoField(primary_key=True, db_column='int_id')
    node = models.ForeignKey('Node', db_column='node')
    mac = models.CharField(max_length=60, blank=True)
    card_power = models.IntegerField()
    card_receive = models.IntegerField(null=True, blank=True)
    card_manufacturer = models.CharField(max_length=75)
    antenna_type = models.CharField(max_length=45)
    antenna_dbi = models.IntegerField()
    cable_loss = models.FloatField(null=True, blank=True)
    channel = models.IntegerField()
    mode = models.CharField(max_length=12, choices=INTERFACE_MODE_CHOICES)
    class_field = models.CharField(max_length=30, choices=NODE_CLASS_CHOICES, db_column='class') # Field renamed because it was a Python reserved word. Field name made lowercase.
    def __unicode__(self):
        return u'%s: %ddBi %s' % (self.node_id, self.antenna_dbi, self.antenna_type)
    class Meta:
        db_table = u'nodes_interfaces'
        ordering = ['node', 'id']
    @property
    def links(self):
        return self.links_1.all() | self.links_2.all()

class NodeIp(models.Model):
    address = models.CharField(max_length=45, primary_key=True)
    subnet = models.IntegerField(null=True, blank=True)
    node = models.ForeignKey('Node', null=True, blank=True, db_column='node_interface')
    type = models.CharField(max_length=24, blank=True)
    area = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return u'%s/%s: %s' % (self.address, self.subnet, self.node)
    class Meta:
        db_table = u'nodes_ips'
        ordering = ['address']

LINK_CLASS_REGULAR = 'regular'
LINK_CLASS_VIRTUAL = 'virtual'
LINK_CLASS_ROUTER = 'router'
LINK_CLASS_BACKBONE = 'backbone'

LINK_CLASS_CHOICES = (
    (LINK_CLASS_REGULAR, 'Regular'),
    (LINK_CLASS_VIRTUAL, 'Virtual'),
    (LINK_CLASS_ROUTER, 'Router'),
    (LINK_CLASS_BACKBONE, 'Backbone'),
)

class Link(models.Model):
    id = models.AutoField(primary_key=True, db_column='link_id')
    interface_1 = models.ForeignKey('Interface', related_name='links_1', db_column='interface_1')
    interface_2 = models.ForeignKey('Interface', related_name='links_2', db_column='interface_2')
    link_class = models.CharField(max_length=24, choices=LINK_CLASS_CHOICES, db_column='class', blank=True) # Field renamed because it was a Python reserved word. Field name made lowercase.
    def __unicode__(self):
        return u'{0}: {1[0]} - {1[1]}'.format(
            self.id,
            sorted([
                self.interface_1,
                self.interface_2,
            ],
            cmp=lambda a, b: cmp(a.node.id, b.node.id)),
        )

    class Meta:
        db_table = u'nodes_links'
        ordering  = ['interface_1', 'interface_2']

    def status(self):
        s1, s2 = self.interface_1.node.status, self.interface_2.node.status
        for (status, description) in NODE_STATUS_CHOICES:
            if status in (s1, s2):
                return status

    def get_status_display(self):
        return dict(NODE_STATUS_CHOICES)[self.status()]

    def get_status_color(self):
        return NODE_STATUS_COLORS[self.status()]

NODE_STATUS_INTERESTED = 'interested'
NODE_STATUS_GATHERING = 'gathering'
NODE_STATUS_BUILDING = 'building'
NODE_STATUS_TESTING = 'testing'
NODE_STATUS_OPERATIONAL = 'operational'

SERVICE_TYPE_DHCP = 'dhcp'
SERVICE_TYPE_DNS = 'dns'
SERVICE_TYPE_FINGER = 'finger'
SERVICE_TYPE_FTP = 'ftp'
SERVICE_TYPE_GAME = 'game_server'
SERVICE_TYPE_IMAP = 'imap'
SERVICE_TYPE_IRC = 'irc'
SERVICE_TYPE_IM = 'im'
SERVICE_TYPE_OTHER = 'other'
SERVICE_TYPE_P2P = 'p2p'
SERVICE_TYPE_POP3 = 'pop3'
SERVICE_TYPE_QOTD = 'qotd'
SERVICE_TYPE_SMTP = 'smtp'
SERVICE_TYPE_SSH = 'ssh'
SERVICE_TYPE_TELNET = 'telnet'
SERVICE_TYPE_WWW = 'www'

SERVICE_TYPE_CHOICES = (
    (SERVICE_TYPE_DHCP, 'DHCP'),
    (SERVICE_TYPE_DNS, 'DNS'),
    (SERVICE_TYPE_FINGER, 'Finger'),
    (SERVICE_TYPE_FTP, 'FTP'),
    (SERVICE_TYPE_GAME, 'Game Server'),
    (SERVICE_TYPE_IMAP, 'IMAP'),
    (SERVICE_TYPE_IRC, 'IRC'),
    (SERVICE_TYPE_IM, 'Instant messaging'),
    (SERVICE_TYPE_OTHER, 'Other'),
    (SERVICE_TYPE_P2P, 'Peer to peer'),
    (SERVICE_TYPE_POP3, 'POP3'),
    (SERVICE_TYPE_QOTD, 'Quote of the day'),
    (SERVICE_TYPE_SMTP, 'SMTP'),
    (SERVICE_TYPE_SSH, 'SSH'),
    (SERVICE_TYPE_TELNET, 'Telnet'),
    (SERVICE_TYPE_WWW, 'www'),
)

class Service(models.Model):
    id = models.AutoField(primary_key=True, db_column='service_id')
    node = models.ForeignKey('Node', db_column='node')
    service_type = models.CharField(max_length=36, choices=SERVICE_TYPE_CHOICES, blank=True, db_column='service_type')
    ip = models.CharField(max_length=45, blank=True, db_column='service_ip')
    port = models.CharField(max_length=15, db_column='service_port')
    description = models.CharField(max_length=300)
    def __unicode__(self):
        return u'%s %s:%s %s' % (self.node_id, self.ip, self.port, self.description)
    class Meta:
        db_table = u'nodes_services'
        ordering = ['ip', 'port', 'description', 'node']

class Statistic(models.Model):
    date = models.DateField(db_column='the_date', primary_key=True)
    operational = models.IntegerField()
    testing = models.IntegerField()
    building = models.IntegerField()
    gathering = models.IntegerField()
    interested = models.IntegerField()
    total = models.IntegerField()
    interfaces = models.IntegerField()
    links = models.IntegerField()
    financial_members = models.IntegerField()
    expired_members = models.IntegerField()
    payment_members = models.IntegerField()
    approval_members = models.IntegerField()
    card_members = models.IntegerField()
    def __unicode__(self):
        return u'%s: %d operatoinal, %d testing, %d building, %d gathering, %d interested' % (self.date, self.operational, self.testing, self.building, self.gathering, self.interested)
    class Meta:
        db_table = u'stats'
        ordering = ['-date']

