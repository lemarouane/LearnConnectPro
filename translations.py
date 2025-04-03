"""
Translation system for the e-learning platform
"""

# French translations
fr = {
    # General UI
    "app_title": "Zouhair E-learning",
    "welcome_message": "Bienvenue sur la plateforme Zouhair E-learning",
    "login": "Connexion",
    "logout": "Déconnexion",
    "register": "S'inscrire",
    "dashboard": "Tableau de bord",
    "profile": "Profil",
    "settings": "Paramètres",
    "search": "Rechercher",
    "submit": "Soumettre",
    "cancel": "Annuler",
    "save": "Enregistrer",
    "delete": "Supprimer",
    "edit": "Modifier",
    "view": "Voir",
    "back": "Retour",
    "next": "Suivant",
    "previous": "Précédent",
    "what_happens_next": "Que se passe-t-il maintenant?",
    "admin_review": "Un administrateur examinera vos détails d'inscription.",
    "once_approved": "Une fois approuvé, vous pourrez accéder au contenu de la plateforme.",
    "will_be_assigned": "Vous serez assigné à des niveaux, des matières et des cours spécifiques en fonction de vos besoins.",
    "thank_you": "Merci pour votre patience!",
    "unknown_role": "Rôle d'utilisateur inconnu. Veuillez contacter le support.",
    
    # Login/Registration
    "username": "Nom d'utilisateur",
    "password": "Mot de passe",
    "confirm_password": "Confirmer le mot de passe",
    "full_name": "Nom complet",
    "email": "Email",
    "phone": "Téléphone",
    "remember_me": "Se souvenir de moi",
    "forgot_password": "Mot de passe oublié ?",
    "login_success": "Connexion réussie !",
    "login_failed": "Échec de la connexion. Veuillez vérifier vos identifiants.",
    "registration_success": "Inscription réussie ! Vous pouvez maintenant vous connecter.",
    "passwords_not_match": "Les mots de passe ne correspondent pas.",
    "username_taken": "Ce nom d'utilisateur est déjà pris.",
    "email_taken": "Cet email est déjà utilisé.",
    "invalid_email": "Veuillez entrer un email valide.",
    "invalid_phone": "Veuillez entrer un numéro de téléphone valide.",
    "required_field": "Ce champ est obligatoire.",
    
    # Dashboard
    "admin_dashboard": "Tableau de bord administrateur",
    "student_dashboard": "Tableau de bord étudiant",
    "overview": "Vue d'ensemble",
    "statistics": "Statistiques",
    "content_management": "Gestion du contenu",
    "user_management": "Gestion des utilisateurs",
    "course_management": "Gestion des cours",
    "level_management": "Gestion des niveaux",
    "subject_management": "Gestion des matières",
    "activity_logs": "Journaux d'activité",
    
    # Content
    "add_content": "Ajouter du contenu",
    "edit_content": "Modifier le contenu",
    "delete_content": "Supprimer le contenu",
    "content_title": "Titre",
    "content_type": "Type de contenu",
    "content_category": "Catégorie",
    "content_difficulty": "Difficulté",
    "content_description": "Description",
    "content_file": "Fichier",
    "content_url": "URL",
    "content_added": "Contenu ajouté avec succès",
    "content_updated": "Contenu mis à jour avec succès",
    "content_deleted": "Contenu supprimé avec succès",
    "assign_content": "Assigner le contenu",
    "unassign_content": "Désassigner le contenu",
    "assigned_users": "Utilisateurs assignés",
    "pdf_document": "Document PDF",
    "youtube_video": "Vidéo YouTube",
    "beginner": "Débutant",
    "intermediate": "Intermédiaire",
    "advanced": "Avancé",
    
    # PDF Viewer
    "pdf_viewer": "Visionneuse PDF",
    "pdf_preview": "Aperçu PDF",
    "page": "Page",
    "take_screenshot": "Prendre une capture d'écran (3 max par 15 minutes)",
    "pdf_protection": "Remarque : Ce document est protégé. Les captures d'écran sont limitées à 3 par 15 minutes et sont surveillées.",
    "pdf_page_limit": "Affichage des 10 premières pages sur {total_pages} au total pour des raisons de performance.",
    "pdf_not_found": "Fichier PDF introuvable.",
    
    # Video Player
    "video_player": "Lecteur vidéo",
    "video_preview": "Aperçu vidéo",
    
    # Users
    "users": "Utilisateurs",
    "add_user": "Ajouter un utilisateur",
    "edit_user": "Modifier l'utilisateur",
    "delete_user": "Supprimer l'utilisateur",
    "user_details": "Détails de l'utilisateur",
    "user_role": "Rôle",
    "admin": "Administrateur",
    "student": "Étudiant",
    "teacher": "Enseignant",
    "active": "Actif",
    "inactive": "Inactif",
    "validate_user": "Valider l'utilisateur",
    "invalidate_user": "Invalider l'utilisateur",
    "user_validated": "Utilisateur validé avec succès",
    "user_invalidated": "Utilisateur invalidé avec succès",
    "last_login": "Dernière connexion",
    "date_joined": "Date d'inscription",
    
    # Levels & Subjects
    "levels": "Niveaux",
    "add_level": "Ajouter un niveau",
    "edit_level": "Modifier le niveau",
    "delete_level": "Supprimer le niveau",
    "level_name": "Nom du niveau",
    "level_description": "Description du niveau",
    "subjects": "Matières",
    "add_subject": "Ajouter une matière",
    "edit_subject": "Modifier la matière",
    "delete_subject": "Supprimer la matière",
    "subject_name": "Nom de la matière",
    "subject_description": "Description de la matière",
    "assign_to_level": "Assigner au niveau",
    
    # Courses
    "courses": "Cours",
    "my_courses": "Mes cours",
    "available_courses": "Cours disponibles",
    "course_details": "Détails du cours",
    "course_content": "Contenu du cours",
    "start_course": "Commencer le cours",
    "continue_course": "Continuer le cours",
    "course_completion": "Achèvement du cours",
    "completed": "Terminé",
    "in_progress": "En cours",
    "not_started": "Non commencé",
    
    # Error messages
    "error": "Erreur",
    "error_occurred": "Une erreur s'est produite",
    "access_denied": "Accès refusé",
    "not_found": "Non trouvé",
    "server_error": "Erreur du serveur",
    "please_login": "Veuillez vous connecter pour accéder à cette page",
    "admin_only": "Cette page est réservée aux administrateurs",
    "validation_required": "Validation du compte requise",
    
    # Messages
    "changes_saved": "Modifications enregistrées avec succès",
    "operation_successful": "Opération réussie",
    "confirmation_required": "Confirmation requise",
    "confirm_delete": "Êtes-vous sûr de vouloir supprimer cet élément ? Cette action est irréversible.",
    "data_updated": "Données mises à jour avec succès",
    
    # Placeholders
    "search_placeholder": "Rechercher...",
    "select_placeholder": "Sélectionner...",
    "description_placeholder": "Entrez une description ici...",
    "no_data": "Aucune donnée disponible",
    "loading": "Chargement...",
}

# Default language dictionary (can be used as a fallback)
default = {
    # We can use the English versions as defaults
    # This would be filled with English translations
}

# Function to get a translation
def get_text(key, lang="fr"):
    """
    Get translated text for a given key.
    
    Args:
        key: The translation key
        lang: Language code (default: 'fr')
        
    Returns:
        Translated text or the key itself if not found
    """
    if lang == "fr":
        return fr.get(key, key)
    return default.get(key, key)

# For convenience, define a shorthand function
def t(key):
    """Shorthand for get_text with default language"""
    return get_text(key)