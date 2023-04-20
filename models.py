class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(64))
  email = db.Column(db.String(64), unique=True)
  password = db.Column(db.String(64))
  users = db.relationship('User', backref='',lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % self.name