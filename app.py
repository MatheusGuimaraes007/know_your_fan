import streamlit as st
import os
from openai import OpenAI

from models.document_validator import DocumentValidator
from models.instagram_validator import InstagramValidator
from models.profile_links_validator import ProfileLinksValidator
from database.db_manager import DBManager

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FanRegistrationApp:
    def __init__(self):
        self.db = DBManager()
        self.document_validator = DocumentValidator()
        self.instagram_validator = InstagramValidator()
        self.profile_links_validator = ProfileLinksValidator()

    def run(self):
        st.set_page_config(layout="centered")
        st.title("Cadastro de Fã da FURIA 🎮🔥")

        # Botão para ir para a dashboard admin
        if st.button("Acessar Admin Dashboard"):
            st.switch_page("admin_dashboard.py")

        if "cadastro_feito" not in st.session_state:
            st.session_state["cadastro_feito"] = False

        if not st.session_state["cadastro_feito"]:
            self.cadastro_form()
        else:
            self.resultado_analise()

    def cadastro_form(self):
        st.subheader("Preencha seus dados:")

        nome = st.text_input("Nome completo")
        endereco = st.text_input("Endereço")
        cpf = st.text_input("CPF (apenas números)")

        opcoes_interesses = [
            "CS:GO", "Valorant", "League of Legends", "Free Fire", 
            "Rainbow Six", "Dota 2", "PUBG", "Rocket League", "Outros"
        ]
        interesses_selecionados = st.multiselect(
            "Quais jogos ou eventos você mais acompanha?",
            options=opcoes_interesses
        )
        interesse_outros = ""
        if "Outros" in interesses_selecionados:
            interesse_outros = st.text_input("Qual outro jogo/evento você acompanha?")

        uploaded_file = st.file_uploader("Envie uma foto do seu RG ou CPF (JPG/PNG)", type=["jpg", "jpeg", "png"])
        instagram_username = st.text_input("Digite seu @username do Instagram")
        links = st.text_area("Cole links de perfis de e-sports (separados por vírgula)")

        atracoes_furia = st.multiselect("O que mais te atrai na FURIA como organização?", [
            "A postura agressiva e competitiva",
            "A identidade brasileira",
            "Os atletas e suas histórias",
            "Os bastidores e conteúdos exclusivos",
            "Os produtos e collabs",
            "O impacto fora do jogo"
        ])

        iniciativas_desejadas = st.multiselect("Quais dessas iniciativas você gostaria de ver a FURIA promovendo?", [
            "Meet & greet com atletas",
            "Torneios comunitários",
            "Workshops de carreira em e-sports",
            "Mentorias com staff",
            "Aulas e treinamentos online",
            "Conteúdos sobre lifestyle"
        ])

        identidade_fan = st.radio("Com qual dessas frases você mais se identifica como fã?", [
            "Torço como se estivesse jogando.",
            "Gosto de acompanhar os bastidores e a rotina.",
            "Curto a marca, mesmo sem assistir todos os jogos.",
            "Sou fã dos jogadores, não só do time.",
            "Gosto de estar por dentro de tudo."
        ])

        produtos_consumo = st.multiselect("Você consome produtos ou serviços relacionados a e-sports?", [
            "Jerseys e camisetas",
            "Acessórios gamer",
            "Cadeiras e móveis gamer",
            "Cursos e mentorias online",
            "Serviços de streaming",
            "Não consumo nada ainda"
        ])

        recomendacao_furia = st.radio("Você já recomendou a FURIA para alguém? Como?", [
            "Já falei com amigos sobre a organização",
            "Já compartilhei conteúdo da FURIA nas redes",
            "Já presenteei alguém com algo da FURIA",
            "Ainda não, mas penso em fazer",
            "Não, ainda não me envolvi tanto"
        ])

        experiencia_desejada = st.radio("Qual dessas experiências seria a mais inesquecível para você?", [
            "Assistir a uma final da FURIA presencialmente",
            "Jogar com um player da FURIA",
            "Ganhar um item exclusivo",
            "Fazer parte de uma ação de bastidores",
            "Receber um reconhecimento como fã"
        ])

        plataforma_membros = st.multiselect("Se a FURIA lançasse uma plataforma para membros, o que você gostaria de acessar?", [
            "Conteúdos exclusivos",
            "Descontos e drops limitados",
            "Recompensas por engajamento",
            "Participação em votações",
            "Ranking de fãs",
            "Sala de bate-papo com outros membros"
        ])

        comunidades_online = st.multiselect("Você participa de quais comunidades online ligadas à FURIA ou e-sports?", [
            "Discord da FURIA",
            "Grupos no WhatsApp/Telegram",
            "Reddit ou fóruns",
            "Grupos no Facebook",
            "Nenhuma no momento"
        ])

        conteudo_preferido = st.multiselect("Qual desses conteúdos você gostaria de ver mais nas redes da FURIA?", [
            "Making of e bastidores",
            "Conteúdo de treino e performance",
            "Vlogs e dia a dia dos jogadores",
            "Memes e cultura gamer",
            "Entrevistas com staff",
            "Collabs com artistas ou marcas"
        ])

        contribuicao_fan = st.multiselect("Você gostaria de contribuir de alguma forma com a FURIA?", [
            "Criando conteúdo",
            "Participando de ações presenciais",
            "Atuando como moderador",
            "Dando ideias para campanhas",
            "Não, prefiro apenas acompanhar"
        ])

        if st.button("Enviar Cadastro"):
            if nome and endereco and cpf:
                st.session_state["carregando"] = True
                with st.spinner("Validando dados..."):

                    doc_validado = self.document_validator.validate(uploaded_file, nome, cpf)
                    insta_validado = self.instagram_validator.validate(instagram_username)
                    links_list = [link.strip() for link in links.split(",") if link.strip()]
                    links_validados = self.profile_links_validator.validate(links_list)

                    interesses_final = interesses_selecionados.copy()
                    if "Outros" in interesses_final and interesse_outros:
                        interesses_final.remove("Outros")
                        interesses_final.append(interesse_outros)
                    interesses_texto = ", ".join(interesses_final)

                    atracoes_furia = atracoes_furia or []
                    iniciativas_desejadas = iniciativas_desejadas or []
                    produtos_consumo = produtos_consumo or []
                    plataforma_membros = plataforma_membros or []
                    comunidades_online = comunidades_online or []
                    conteudo_preferido = conteudo_preferido or []
                    contribuicao_fan = contribuicao_fan or []
                    identidade_fan = identidade_fan or ""
                    recomendacao_furia = recomendacao_furia or ""
                    experiencia_desejada = experiencia_desejada or ""

                    self.db.save_user(
                        nome=nome,
                        endereco=endereco,
                        cpf=cpf,
                        interesses=interesses_texto,
                        doc_validado=doc_validado,
                        instagram_username=instagram_username,
                        insta_validado=insta_validado,
                        links=links_list,
                        links_validados=len(links_validados),
                        atracoes_furia=atracoes_furia,
                        iniciativas_desejadas=iniciativas_desejadas,
                        identidade_fan=identidade_fan,
                        produtos_consumo=produtos_consumo,
                        recomendacao_furia=recomendacao_furia,
                        experiencia_desejada=experiencia_desejada,
                        plataforma_membros=plataforma_membros,
                        comunidades_online=comunidades_online,
                        conteudo_preferido=conteudo_preferido,
                        contribuicao_fan=contribuicao_fan
                    )

                    st.session_state["doc_validado"] = doc_validado

                    prompt = (
                        f"Meu nome é {nome}. Aqui estão minhas informações como fã:\n\n"
                        f"- Meus interesses: {interesses_texto}.\n"
                        f"- Meu Instagram é @{instagram_username} (validado: {'sim' if insta_validado else 'não'}).\n"
                        f"- Enviei {len(links_list)} links, e {len(links_validados)} foram validados como relevantes.\n"
                        f"- Meu documento foi validado por IA? {'Sim' if doc_validado else 'Não'}.\n"
                        f"- Me identifico como fã da seguinte forma: {identidade_fan}\n"
                        f"- O que mais me atrai na FURIA: {', '.join(atracoes_furia)}\n"
                        f"- Iniciativas que gostaria de ver: {', '.join(iniciativas_desejadas)}\n"
                        f"- Produtos e serviços que consumo: {', '.join(produtos_consumo)}\n"
                        f"- Já recomendei a FURIA? {recomendacao_furia}\n"
                        f"- Experiência inesquecível desejada: {experiencia_desejada}\n"
                        f"- Gostaria de acessar na plataforma membros: {', '.join(plataforma_membros)}\n"
                        f"- Comunidades online que participo: {', '.join(comunidades_online)}\n"
                        f"- Conteúdos preferidos: {', '.join(conteudo_preferido)}\n"
                        f"- Como gostaria de contribuir: {', '.join(contribuicao_fan)}\n\n"
                        f"Com base nessas informações, diga com empatia se eu pareço um fã engajado com e-sports "
                        f"e se tenho perfil de fã da FURIA. Fale comigo diretamente, em primeira pessoa, de forma sincera, direta e acolhedora."
                        f"Não diga nada do tipo: 'Estou à disposição'. Use frases como: 'Você parece...', 'Talvez você ainda...', 'Eu diria que você...'."
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Você é um analista da FURIA que fala com fãs de forma direta, empática e humana."},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    st.session_state["resposta_ia"] = response.choices[0].message.content
                    st.session_state["cadastro_feito"] = True
                    st.rerun()
            else:
                st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

    def resultado_analise(self):
        st.subheader("📊 Resultado da Análise")
        st.success("✅ Cadastro realizado com sucesso!")

        # Mostrar status da validação do documento
        if "doc_validado" in st.session_state:
            if st.session_state["doc_validado"]:
                st.success("📄 Documento validado com sucesso!")
            else:
                st.error("📄 Documento não foi validado automaticamente. Será necessário verificar manualmente.")

        st.info("🧠 Análise da IA sobre seu perfil como fã da FURIA:")
        st.markdown(st.session_state["resposta_ia"])

        if st.button("Novo Cadastro"):
            st.session_state["cadastro_feito"] = False
            st.rerun()

if __name__ == "__main__":
    app = FanRegistrationApp()
    app.run()
