from datetime import date

from app import crud
from app.database import Base, SessionLocal, engine

def main():
    Base.metadata.create_all(bind=engine)
    print("[OK] Tabelas criadas: tutores, animais, atendimentos.")

    hoje = date.today().strftime("%d/%m/%Y")
    db = SessionLocal()

    try:
        tutor1 = crud.inserir_tutor(
            db, "Kevin Campos Liell", "(61) 99999-2222", "kakakakak@email.com"
        )
        tutor2 = crud.inserir_tutor(
            db, "Nathã Braga Oliveira", "(61) 99999-0002", "nanananan@email.com"
        )
        print(f"[OK] Tutores inseridos: {tutor1.nome_completo} (id={tutor1.id}), "
              f"{tutor2.nome_completo} (id={tutor2.id}).")

        animal1 = crud.inserir_animal(db, "Naia", "cobra", "Naja", 3.5, tutor1.id)
        animal2 = crud.inserir_animal(db, "Miau", "jaguatirica", "", 12.2, tutor1.id)
        animal3 = crud.inserir_animal(db, "Nath", "hamster", "Sírio", 0.32, tutor2.id)
        print(f"[OK] Animais inseridos: {animal1.nome_animal} (id={animal1.id}), "
              f"{animal2.nome_animal} (id={animal2.id}), "
              f"{animal3.nome_animal} (id={animal3.id}).")

        at1 = crud.inserir_atendimento(db, hoje, "Manejo da ecdise", 300.00, animal1.id)
        at2 = crud.inserir_atendimento(db, hoje, "Vacina Polivalente Inativada", 220.00, animal2.id)
        at3 = crud.inserir_atendimento(db, hoje, "Desgaste e Alinhamento de Dentes", 150.00, animal3.id)
        print(f"[OK] Atendimentos inseridos em {hoje}: ids {at1.id}, {at2.id}, {at3.id}.")

        print("[OK] Sistema VidaPet funcionando corretamente.")
    finally:
        db.close()


if __name__ == "__main__":
    main()