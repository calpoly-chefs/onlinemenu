from sqlalchemy.ext.hybrid import hybrid_property
from .. import db

class Image(db.Model):
    """Image model for storing image metadata"""
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("user.username"))
    user = db.relationship("User")
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    @hybrid_property
    def profile_image(self):
        return self.user.profile_images

    @hybrid_property
    def is_remix(self):
        return self.recipe.parent_id is not None

    def __repr__(self):
        return self.url
