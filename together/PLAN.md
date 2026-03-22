# Together - Plan de développement

## Stack technique choisie

| Composant | Choix | Pourquoi |
|---|---|---|
| **Framework** | Next.js 14 (App Router) | SSR, API routes intégrées, PWA-friendly |
| **UI** | Material UI (MUI) v5 | Material Design natif, composants riches |
| **Calendrier** | FullCalendar React | Robuste, vue mois, drag & drop |
| **Auth** | Supabase Auth (magic link) | Magic link email out-of-the-box |
| **Base de données** | Supabase (PostgreSQL) | Temps réel, Row Level Security, gratuit pour commencer |
| **i18n** | next-intl | Léger, adapté à Next.js App Router |
| **Déploiement** | Vercel | Déploiement instantané, preview par PR |

---

## Milestone 1 — Fondations & Auth
**Objectif : tu peux ouvrir l'app, t'inscrire via magic link, et voir ton profil.**

- [ ] Init projet Next.js + TypeScript + MUI + Supabase
- [ ] Config PWA (manifest.json, service worker basique)
- [ ] Mise en place Supabase (projet, tables users/profiles)
- [ ] Page d'accueil / landing
- [ ] Auth magic link : page login, callback, session
- [ ] Page profil utilisateur (nom, avatar, langue FR/EN)
- [ ] Layout global avec navbar et navigation
- [ ] Setup i18n (FR + EN)

**Tu peux tester :**
- Ouvrir l'app dans le navigateur
- Recevoir un magic link par email et te connecter
- Voir/éditer ton profil
- Changer la langue FR/EN
- Installer la PWA sur mobile

---

## Milestone 2 — Groupes
**Objectif : tu peux créer un groupe, inviter ta famille, et gérer les membres.**

- [ ] Tables Supabase : groups, group_members
- [ ] Page "Mes groupes" (liste des groupes)
- [ ] Créer un groupe (nom, description)
- [ ] Page groupe avec liste des membres
- [ ] Système d'invitation par lien unique
- [ ] Système d'invitation par email
- [ ] Gestion des rôles (admin/membre)
- [ ] Quitter un groupe (transfert auto d'admin si créateur)
- [ ] Supprimer un groupe (admin uniquement)

**Tu peux tester :**
- Créer un groupe "Famille Dupont"
- Générer un lien d'invitation et l'envoyer
- Un autre compte rejoint via le lien
- Voir les membres du groupe
- L'admin peut retirer un membre

---

## Milestone 3 — Calendrier personnel
**Objectif : chaque utilisateur peut gérer ses événements dans son calendrier perso.**

- [ ] Table Supabase : events (avec type, dates, lieu, visibilité)
- [ ] Types d'événements prédéfinis : Vacances, Disponible, Voyage + custom
- [ ] Page "Mon calendrier" avec vue mois (FullCalendar)
- [ ] Créer un événement (titre, type, date début/fin, journée entière ou horaire)
- [ ] Champ lieu en texte libre
- [ ] Modifier / supprimer un événement
- [ ] Marquer un événement comme privé (apparaîtra "occupé" dans le groupe)

**Tu peux tester :**
- Voir ton calendrier personnel en vue mois
- Ajouter "Vacances en Bretagne" du 1er au 15 août
- Ajouter "Dispo weekend" le samedi 5 avril (créneau horaire)
- Créer un type custom "Télétravail"
- Marquer un événement comme privé
- Modifier et supprimer des événements

---

## Milestone 4 — Calendrier de groupe
**Objectif : le calendrier partagé agrège les événements de tous les membres. C'est le coeur de l'app.**

- [ ] Page calendrier de groupe (vue mois, FullCalendar)
- [ ] Affichage des événements de tous les membres avec couleur par membre
- [ ] Attribution automatique des couleurs par membre
- [ ] Filtres : cocher/décocher les membres à afficher
- [ ] Événements privés affichés comme "Occupé" (sans détails)
- [ ] Clic sur un événement → détail (titre, lieu, dates, qui)
- [ ] Légende des couleurs / membres
- [ ] Row Level Security Supabase (un membre ne voit que les groupes auxquels il appartient)

**Tu peux tester :**
- Ouvrir le calendrier du groupe "Famille Dupont"
- Voir les vacances de chaque membre dans une couleur différente
- Filtrer pour ne voir que 2 membres sur 4
- Un événement privé apparaît comme "Occupé" sans détail
- Cliquer sur un événement pour voir les infos

---

## Milestone 5 — Multi-groupes & polish
**Objectif : navigation fluide entre groupes, UX polie, app prête à utiliser au quotidien.**

- [ ] Dashboard d'accueil : vue rapide de tous tes groupes + prochains événements
- [ ] Switcher de groupe fluide dans la navbar
- [ ] Le calendrier perso synchronise vers tous tes groupes automatiquement
- [ ] Responsive design vérifié (mobile, tablette, desktop)
- [ ] PWA : icône, splash screen, manifest complet
- [ ] Pages d'erreur (404, etc.)
- [ ] Loading states et feedback utilisateur (toasts, skeletons)
- [ ] Sécurité : audit RLS, validation des inputs

**Tu peux tester :**
- Être dans 3 groupes différents et naviguer entre eux
- Ajouter un événement dans ton calendrier perso → il apparaît dans tous tes groupes
- Utiliser l'app sur mobile comme une app native (PWA installée)
- Tout fonctionne de manière fluide et intuitive

---

## Ce qui est prévu "Plus tard" (post-V1)
- Événements récurrents
- Statut tentatif/confirmé
- Import/export iCal + synchro Google Calendar
- Détection automatique des chevauchements + suggestions de créneaux communs
- Notifications push
- Mode offline
- Dark mode
