import sqlite3
import json
from datetime import datetime
import os

class DBManager:
    def __init__(self, db_path='data/users.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fans_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                endereco TEXT,
                cpf TEXT,
                interesses TEXT,
                doc_validado BOOLEAN,
                instagram_username TEXT,
                insta_validado BOOLEAN,
                links TEXT,
                links_validados TEXT,
                atracoes_furia TEXT,
                iniciativas_desejadas TEXT,
                identidade_fan TEXT,
                produtos_consumo TEXT,
                recomendacao_furia TEXT,
                experiencia_desejada TEXT,
                plataforma_membros TEXT,
                comunidades_online TEXT,
                conteudo_preferido TEXT,
                contribuicao_fan TEXT,
                data_envio TEXT
            )
        ''')
        self.conn.commit()

    def save_user(self, nome, endereco, cpf, interesses, doc_validado, instagram_username, insta_validado, links, links_validados,
                  atracoes_furia, iniciativas_desejadas, identidade_fan, produtos_consumo, recomendacao_furia, experiencia_desejada,
                  plataforma_membros, comunidades_online, conteudo_preferido, contribuicao_fan):

        data_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute('''
            INSERT INTO fans_data (
                nome, endereco, cpf, interesses, doc_validado,
                instagram_username, insta_validado, links, links_validados,
                atracoes_furia, iniciativas_desejadas, identidade_fan,
                produtos_consumo, recomendacao_furia, experiencia_desejada,
                plataforma_membros, comunidades_online, conteudo_preferido,
                contribuicao_fan, data_envio
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nome,
            endereco,
            cpf,
            interesses,
            doc_validado,
            instagram_username,
            insta_validado,
            ', '.join(links),
            str(links_validados),
            ', '.join(atracoes_furia),
            ', '.join(iniciativas_desejadas),
            identidade_fan,
            ', '.join(produtos_consumo),
            recomendacao_furia,
            experiencia_desejada,
            ', '.join(plataforma_membros),
            ', '.join(comunidades_online),
            ', '.join(conteudo_preferido),
            ', '.join(contribuicao_fan),
            data_envio
        ))
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM fans_data')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
