import sqlite3

preset_table_name = "commandPreset"


class Database:
    def __init__(self):
        db_name = "./database.db"
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def execute(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def fetch(self, query, values):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    # 关闭连接
    def close(self):
        self.connection.close()

    def create_present_table(self):
        cursor = self.connection.cursor()
        result = cursor.execute('select * from sqlite_master where name = "%s";' % preset_table_name)
        # 将初始预设写入数据库
        if result.fetchone() is None:
            cursor.execute(
                """create table %s (
                            id integer primary key autoincrement,
                            name text,
                            outputOption TEXT,
                            description TEXT
                            )"""
                % (preset_table_name)
            )

            # 新建一个空预设
            # 不使用预设
            presetName = "不使用预设"
            cursor.execute(
                """
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s',
                            ''
                            );"""
                % (preset_table_name, presetName)
            )

            # 中日英字幕
            presetName = "中日英字幕"
            description = ""
            cursor.execute(
                """
                            insert into %s
                            (name, outputOption, description)
                            values (
                            '%s',
                            '--embed-subs --sub-langs "zh.*,en.*,ja"',
                            '%s'
                            );"""
                % (preset_table_name, presetName, description)
            )

            # 中文,英语,日语字幕 vtt-->srt
            presetName = "中日英字幕 vtt-->srt"
            description = ""
            cursor.execute(
                """
                            insert into %s
                            (name, outputOption, description)
                            values (
                            '%s',
                            '--embed-subs --sub-langs "zh.*,en.*,ja" --sub-format vtt --convert-subs srt',
                            '%s'
                            );"""
                % (preset_table_name, presetName, description)
            )

        else:
            print('存储"预设"的表单已存在')

        self.connection.commit()
        return True
