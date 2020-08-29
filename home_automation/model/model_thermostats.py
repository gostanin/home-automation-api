from datetime import datetime

from home_automation.model.model import Model


class ModelThermostats(Model):
    def get_thermostats(self):
        sql = """SELECT * FROM thermostats"""
        return self._exec(sql)

    def get_thermostat(self, id):
        sql = """SELECT * FROM thermostats WHERE id=?"""
        return self._exec(sql, (id,))

    def save_thermostat(self, name, temp):
        sql = """INSERT INTO thermostats(name, temp, creation_date)
                 VALUES(?, ?, ?)"""
        creation_date = datetime.now()  # DOCUMENT-IT
        return self._exec(sql, (name, temp, creation_date))

    def delete_thermostat(self, id):
        sql = """DELETE FROM thermostats WHERE id=?"""
        return self._exec(sql, (id,))

    def update_temp(self, id, temp):
        sql = """UPDATE thermostats SET temp=? WHERE id=?"""
        return self._exec(sql, (temp, id))

    def update_name(self, id, name):
        sql = """UPDATE thermostats SET name=? WHERE id=?"""
        return self._exec(sql, (name, id))
