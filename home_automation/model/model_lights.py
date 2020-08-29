from datetime import datetime

from home_automation.model.model import Model


class ModelLights(Model):
    def get_lights(self):
        sql = """SELECT * FROM lights"""
        return self._exec(sql)

    def get_light(self, id):
        sql = """SELECT * FROM lights WHERE id=?"""
        return self._exec(sql, (id,))

    def save_light(self, name, status=0):
        sql = """INSERT INTO lights(name, status, creation_date)
                 VALUES(?, ?, ?)"""
        creation_date = datetime.now()  # DOCUMENT-IT
        return self._exec(sql, (name, status, creation_date))

    def delete_light(self, id):
        sql = """DELETE FROM lights WHERE id=?"""
        return self._exec(sql, (id,))

    def update_status(self, id, status):
        sql = """UPDATE lights SET status=? WHERE id=?"""
        return self._exec(sql, (status, id))

    def update_name(self, id, name):
        sql = """UPDATE lights SET name=? WHERE id=?"""
        return self._exec(sql, (name, id))