from app.extensions import db


def count_increment(name):
    count = Count.query.filter_by(name=name).first()
    if count is None:
        count = Count(
            name=name,
            count=0
        )

    count.count += 1
    db.session.add(count)

    db.session.commit()


def get_count(name):
    count = Count.query.filter_by(name=name).first()
    if count is None:
        count = Count(
            name=name,
            count=0
        )

    return count.count


class Count(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False)
    count = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Count {self.name}: {self.count}>'