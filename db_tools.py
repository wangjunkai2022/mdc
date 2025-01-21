import os
import sqlite3
import config


class VideoData:
    # 原始视频路径
    original_path = None
    # 当前视频的番号
    video_number = None
    # 收刮到的数据
    scrape_data = None
    # 使用的工具名称
    tool_name = None
    # 软连接路径
    soft_link_path = None
    # 硬连接路径
    hard_link_path = None
    # 复制到的路径
    copied_path = None
    # 移动到的路径
    moved_path = None

    def __init__(
        self,
        original_path: str,
        video_number=None,
        scrape_data=None,
        tool_name=None,
        soft_link_path=None,
        hard_link_path=None,
        copied_path=None,
        moved_path=None,
    ):
        """
        初始化 VideoData 实例。
        """
        if original_path:
            existing_data = self.get_by_original_path(original_path, False)
            if existing_data:
                # 如果找到已经存在的数据，则用它初始化实例
                self.original_path = existing_data["original_path"]
                self.video_number = existing_data["video_number"]
                self.scrape_data = existing_data["scrape_data"]
                self.tool_name = existing_data["tool_name"]
                self.soft_link_path = existing_data["soft_link_path"]
                self.hard_link_path = existing_data["hard_link_path"]
                self.copied_path = existing_data["copied_path"]
                self.moved_path = existing_data["moved_path"]
            else:
                # 如果没有找到，则使用提供的参数初始化
                self.original_path = original_path
                self.video_number = video_number
                self.scrape_data = scrape_data
                self.tool_name = tool_name
                self.soft_link_path = soft_link_path
                self.hard_link_path = hard_link_path
                self.copied_path = copied_path
                self.moved_path = moved_path

    def save_to_db(self):
        """将当前 VideoData 实例保存到数据库。"""
        try:
            db_connection = _get_db()
            with db_connection:
                cursor = db_connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO videos (
                        original_path, 
                        video_number, 
                        scrape_data, 
                        tool_name,
                        soft_link_path, 
                        hard_link_path, 
                        copied_path, 
                        moved_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(original_path) DO UPDATE SET
                        video_number = excluded.video_number,
                        scrape_data = excluded.scrape_data,
                        tool_name = excluded.tool_name,
                        soft_link_path = excluded.soft_link_path,
                        hard_link_path = excluded.hard_link_path,
                        copied_path = excluded.copied_path,
                        moved_path = excluded.moved_path
                    """,
                    (
                        self.original_path,
                        self.video_number,
                        self.scrape_data,
                        self.tool_name,
                        self.soft_link_path,
                        self.hard_link_path,
                        self.copied_path,
                        self.moved_path,
                    ),
                )
                print(f"记录已插入或更新: {self.original_path}")
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    @classmethod
    def get_by_original_path(cls, original_path, object: True):
        """
        根据原始视频路径从数据库中获取 VideoData 实例。

        :param original_path: 要查询的原始视频路径
        :return: VideoData 实例或 None
        """
        db_connection = _get_db()
        try:
            with db_connection:
                cursor = db_connection.cursor()
                cursor.execute(
                    """
                    SELECT original_path, video_number, scrape_data, tool_name,
                           soft_link_path, hard_link_path, copied_path, moved_path
                    FROM videos 
                    WHERE original_path = ?
                    """,
                    (original_path,),
                )
                row = cursor.fetchone()  # 只取第一条匹配记录

                if row:
                    if object:
                        return cls(*row)  # 返回一个 VideoData 实例
                    else:
                        # 使用字典保存查询结果
                        keys = [
                            "original_path",
                            "video_number",
                            "scrape_data",
                            "tool_name",
                            "soft_link_path",
                            "hard_link_path",
                            "copied_path",
                            "moved_path",
                        ]
                        return dict(zip(keys, row))  # 返回字典
                else:
                    print(f"未找到原始视频路径 '{original_path}' 的记录。")
                    return None

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            return None

    @classmethod
    def get_by_video_number(cls, video_number):
        """
        根据视频番号从数据库中获取所有 VideoData 实例。

        :param video_number: 要查询的视频番号
        :return: VideoData 实例列表或空列表
        """
        db_connection = _get_db()
        video_data_list = []
        try:
            with db_connection:
                cursor = db_connection.cursor()
                cursor.execute(
                    """
                    SELECT original_path, video_number, scrape_data, tool_name,
                           soft_link_path, hard_link_path, copied_path, moved_path
                    FROM videos 
                    WHERE video_number = ?
                    """,
                    (video_number,),
                )
                rows = cursor.fetchall()  # 获取所有匹配的记录
                for row in rows:
                    video_data_list.append(
                        cls(*row)
                    )  # 每一行数据创建一个 VideoData 实例

                if not video_data_list:
                    print(f"未找到视频番号 '{video_number}' 的记录。")

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

        return video_data_list  # 返回 VideoData 实例列表


def _get_db():
    """获取数据库连接，如果数据库文件不存在则创建新的文件。"""
    db_file = config.getInstance().sql_path()

    db_exists = os.path.exists(db_file)

    db_connection = sqlite3.connect(db_file)

    if not db_exists:
        print(f"数据库文件 '{db_file}' 不存在，正在创建新文件...")
        with db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_path TEXT UNIQUE,  -- 添加 UNIQUE 约束
                    video_number TEXT,
                    scrape_data TEXT,
                    tool_name TEXT,
                    soft_link_path TEXT,
                    hard_link_path TEXT,
                    copied_path TEXT,
                    moved_path TEXT
                )
                """
            )
    else:
        print(f"使用已有的数据库文件 '{db_file}'")

    return db_connection


if __name__ == "__main__":
    # save
    vd = VideoData("/masdja/asdjk/mou1m.mp4")
    vd.video_number = "moum"
    vd.copied_path = "/sss/moum.mp4"
    vd.save_to_db()
    ls = VideoData.get_by_video_number("moum")
    print(ls)
    vd = VideoData("/masdja/asdjk/mou2m.mp4")
    vd.video_number = "moum"
    vd.copied_path = "/sss/moum2.mp4"
    vd.save_to_db()
    ls = VideoData.get_by_video_number("moum")
    print(ls)
    vd = VideoData("/masdja/asdjk/moum.mp4")
    vd.video_number = "moum"
    vd.copied_path = "/sss/moum1.mp4"
    vd.save_to_db()
    ls = VideoData.get_by_video_number("moum")
    print(ls)
    vd = VideoData("/masdja/asdjk/moum.mp4")
    vd.video_number = "moum"
    vd.copied_path = "/sss/moum0.mp4"
    vd.save_to_db()
    ls = VideoData.get_by_video_number("moum")
    print(ls)

    # vd = VideoData("/masdja/asdjk/mou1m.mp4")
    # print(vd.__dict__)
