import os
import rpyc
import marshmallow


class MembreSchema(marshmallow.Schema):
    nom = marshmallow.fields.Str(
        required=True, error_messages={
            'required': 'Le nom est obligatoire.'})
    prenom = marshmallow.fields.Str(
        required=True, error_messages={
            'required': 'Le prénom est obligatoire.'})
    tel = marshmallow.fields.Str(validate=marshmallow.validate.Regexp(
        regex=r'^\d{8}$', error="Format de numéro de téléphone invalide"))
    email = marshmallow.fields.Email(
        error_messages={
            'invalid': 'Adresse email invalide.'})
    fonction = marshmallow.fields.Str(validate=marshmallow.validate.OneOf(
        ['Enseignant', 'Administratif'], error="Valeur invalide pour la fonction"))


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def wait_for_any_press_and_clear():
    input(' ')
    clear()


def print_menu():
    print('************************ MENU ************************')
    print('1- Ajouter nouveau membre')
    print('2- Chercher membre')
    print('3- Afficher annuaire')
    print('4- Afficher enseignants')
    print('5- Afficher administratifs')
    print('6- Quitter')
    print('******************************************************')


def take_option():
    try:
        choice = int(input('Sélectionnez une option: '))
        if choice not in range(1, 7):
            clear()
            print('[error]: please make sure to pass an integer value between 1 and 6!')
            return -1
        return choice
    except Exception:
        clear()
        print('[error]: please make sure to pass an integer value!')
        return -1


def main():
    connection = rpyc.connect('localhost', 33333)
    app = connection.root.get_app_instance()

    while True:
        print_menu()
        option = take_option()
        # handle taked option
        if option == -1:
            pass
        elif option == 1:
            nom = input('Tapez le nom: ')
            prenom = input('Tapez le prénom: ')
            tel = input('Tapez le numéro de téléphone: ')
            fonction = input('Tapez la fonction (Enseignant/Administratif): ')

            membre = {
                'nom': nom,
                'prenom': prenom,
                'tel': tel,
                'email': f'{nom}.{prenom}@esen.tn',
                'fonction': fonction
            }

            try:
                membre_schema = MembreSchema()
                membre_schema.load(membre)
                app.ajouter_membre(membre)
                print('✅ Membre ajouté avec succès!')
            except marshmallow.ValidationError as err:
                print('❌ Membre n\'est pas ajouté!')
                print(f'===> [error]: {err.messages}')
        elif option == 2:
            nom = input('Tapez le nom du membre à chercher: ')
            membre = app.chercher_membre(nom)
            if membre is None:
                print('ℹ️ Membre non trouvé!')
            else:
                print(f"ℹ️ Membre trouvé: ")
                print(f"===> Numéro de téléphone: {membre['tel']}")
                print(f"===> Email: {membre['email']}")
        elif option == 3:
            membres_annuaire = app.afficher_annuaire()
            print(f'ℹ️ Voici l\'annuaire: {membres_annuaire}')
        elif option == 4:
            enseignants = app.afficher_enseignants()
            print(f'ℹ️ Voici les enseignants: {enseignants}')
        elif option == 5:
            administratifs = app.afficher_administratifs()
            print(f'ℹ️ Voici les administratifs: {administratifs}')
        else:
            break
        # wait for any press then clear the screen and loop again
        wait_for_any_press_and_clear()


if __name__ == '__main__':
    main()
