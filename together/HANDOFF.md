# Together - Handoff complet pour nouvelle session

> **Date** : 22 mars 2026
> **Repo** : `tontonkiller/agency-agents` (sous-dossier `together/`)
> **Objectif** : App calendrier familial en PWA

---

## TL;DR - C'est quoi Together ?

Une **PWA de calendrier familial**. Chaque membre de la famille ajoute ses vacances/dispos dans son calendrier perso, et tout le monde voit un calendrier de groupe agrégé avec les événements de chacun (couleur par membre). Les événements privés apparaissent comme "Occupé".

**Stack** : Next.js 16 (App Router) + React 19 + MUI v7 + Supabase (Auth magic link + PostgreSQL + RLS) + next-intl (FR/EN) + FullCalendar

---

## Etat d'avancement

### Milestone 1 — Fondations & Auth : EN COURS (~80%)

**Ce qui est FAIT :**
- [x] Init projet Next.js + TypeScript + MUI + Supabase
- [x] Config PWA (manifest.ts, icones 192/512)
- [x] Supabase : tables profiles + groups + group_members + events + event_types + invitations + RLS complètes
- [x] Page d'accueil / landing
- [x] Auth magic link : page login, callback, session
- [x] Page profil utilisateur (nom, avatar initiale, langue FR/EN)
- [x] Layout global avec TopBar + BottomNav
- [x] Setup i18n (FR + EN, 62 strings)
- [x] Middleware (Supabase session refresh + i18n routing)
- [x] Dashboard avec liste des groupes

**Ce qui MANQUE pour finir le Milestone 1 :**
- [ ] Tester le flow complet auth (magic link → dashboard)
- [ ] Service worker basique pour PWA
- [ ] Vérifier que le build passe proprement (`npm run build`)

### Milestones suivants : PAS COMMENCES
- Milestone 2 : Groupes (création, invitation, membres)
- Milestone 3 : Calendrier personnel (FullCalendar)
- Milestone 4 : Calendrier de groupe (agrégé, couleurs, filtres)
- Milestone 5 : Multi-groupes & polish

---

## Architecture du projet

```
together/
├── PLAN.md                    # Roadmap 5 milestones
├── HANDOFF.md                 # CE FICHIER
├── agents/                    # Personnalités agents (specs, archi, UX, QA)
│   ├── expert-architect.md
│   ├── qa-tester.md
│   ├── spec-master.md
│   └── ui-ux-expert.md
└── app/                       # Application Next.js
    ├── package.json
    ├── tsconfig.json
    ├── next.config.ts
    ├── .env.local             # Credentials Supabase
    ├── supabase/
    │   └── schema.sql         # Schema complet (6 tables + RLS + triggers)
    ├── public/
    │   └── icons/             # icon-192.png, icon-512.png
    └── src/
        ├── proxy.ts           # Middleware (Supabase + i18n)
        ├── app/
        │   ├── layout.tsx     # Root layout
        │   ├── manifest.ts    # PWA manifest
        │   ├── globals.css
        │   └── [locale]/
        │       ├── layout.tsx           # NextIntlClientProvider + ThemeRegistry
        │       ├── page.tsx             # Landing page
        │       ├── login/page.tsx       # Magic link login
        │       ├── auth/callback/route.ts  # Auth callback + auto-create profile
        │       ├── dashboard/
        │       │   ├── layout.tsx
        │       │   ├── page.tsx         # Server: fetch profile + groups
        │       │   └── DashboardContent.tsx  # Client: UI groupes
        │       └── profile/
        │           ├── page.tsx         # Server: fetch profile
        │           └── ProfileContent.tsx  # Client: edit profil + logout
        ├── components/layout/
        │   ├── ThemeRegistry.tsx         # MUI ThemeProvider + CssBaseline
        │   ├── AuthenticatedLayout.tsx   # Shell: TopBar + main + BottomNav
        │   ├── TopBar.tsx               # Header: "Together" + toggle FR/EN
        │   └── BottomNav.tsx            # Footer: Calendrier | Groupes | Profil
        └── lib/
            ├── theme.ts                 # MUI theme (couleurs, typo, spacing)
            ├── i18n/
            │   ├── config.ts            # locales: ['fr', 'en'], default: 'fr'
            │   ├── routing.ts           # defineRouting
            │   ├── navigation.ts        # Link, redirect, usePathname, useRouter
            │   ├── request.ts           # getRequestConfig
            │   └── messages/
            │       ├── fr.json          # 62 strings FR
            │       └── en.json          # 62 strings EN
            ├── supabase/
            │   ├── client.ts            # createBrowserClient
            │   ├── server.ts            # createServerClient (cookies)
            │   └── middleware.ts         # updateSession (refresh auth)
            └── utils/
                └── colors.ts            # 10 couleurs membres
```

---

## Supabase

### Credentials (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=https://vrnctjpxmrdiuiwyxhll.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_A8flMP9xe9xkJ7l2IVOOMA_43SZ_zC_
```

### Schema SQL complet (6 tables)

```sql
-- PROFILES (extends auth.users)
create table if not exists profiles (
  id uuid references auth.users on delete cascade primary key,
  display_name text not null,
  avatar_url text,
  preferred_locale text default 'fr' check (preferred_locale in ('fr', 'en')),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- GROUPS
create table if not exists groups (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  created_by uuid references profiles(id) not null,
  invite_code text unique default encode(gen_random_bytes(6), 'hex'),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- GROUP MEMBERS
create table if not exists group_members (
  id uuid primary key default gen_random_uuid(),
  group_id uuid references groups(id) on delete cascade not null,
  user_id uuid references profiles(id) on delete cascade not null,
  role text not null default 'member' check (role in ('admin', 'member')),
  color text not null default '#1976D2',
  joined_at timestamptz default now(),
  unique(group_id, user_id)
);

-- EVENT TYPES (predefined + custom)
create table if not exists event_types (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  icon text,
  is_system boolean default false,
  created_by uuid references profiles(id),
  created_at timestamptz default now()
);
-- Seed: Vacances (BeachAccess), Disponible (EventAvailable), Voyage (Flight)

-- EVENTS
create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade not null,
  event_type_id uuid references event_types(id),
  title text not null,
  description text,
  location text,
  start_date date not null,
  end_date date not null,
  start_time time,       -- null = journée entière
  end_time time,
  is_all_day boolean default true,
  is_private boolean default false,  -- "Occupé" dans le groupe
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- INVITATIONS
create table if not exists invitations (
  id uuid primary key default gen_random_uuid(),
  group_id uuid references groups(id) on delete cascade not null,
  invited_email text,
  invited_by uuid references profiles(id) not null,
  status text default 'pending' check (status in ('pending', 'accepted', 'expired')),
  expires_at timestamptz default now() + interval '7 days',
  created_at timestamptz default now()
);
```

### RLS (Row Level Security) - résumé

| Table | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| profiles | Tous les auth users | Own (id = auth.uid()) | Own | - |
| groups | Membres du groupe | created_by = auth.uid() | Admins du groupe | Admins du groupe |
| group_members | Membres du même groupe | user_id = auth.uid() | Admins du groupe | Admins OU soi-même |
| event_types | Tous les auth users | Own + is_system=false | - | - |
| events | Owner + co-membres de groupe | Owner | Owner | Owner |
| invitations | Membres du groupe | Admins | - | - |

### Triggers
- `update_updated_at()` sur profiles, groups, events

---

## Design System

### Couleurs
```
Primary:       #1976D2 (Blue)
Secondary:     #FF9800 (Orange)
Background:    #FAFAFA
Surface:       #FFFFFF
Text Primary:  #212121
Text Secondary:#757575
Error:         #D32F2F
Success:       #388E3C
```

### Couleurs membres (auto-assignées dans le calendrier de groupe)
```
1: #1976D2 Blue     2: #D32F2F Red       3: #388E3C Green
4: #7B1FA2 Purple   5: #F57C00 Orange    6: #00838F Teal
7: #C2185B Pink     8: #455A64 Blue Grey  9: #AFB42B Lime
10: #5D4037 Brown
```

### Typo
Roboto. H1: 2rem/700, H2: 1.5rem/600, H3: 1.25rem/600, Body1: 1rem, Body2: 0.875rem, Button: 0.875rem/500

### Spacing : base 8px. Border radius: 8px (cards: 12px)

### MUI overrides : Buttons textTransform=none, padding 10px 24px

---

## Principes UX

- **Three-Tap Rule** : toute action core en 3 taps max
- **Mobile-first** : 375px (iPhone SE) en premier
- **Bottom nav** : Calendrier | Groupes | Profil (thumb-friendly)
- **Accessibilité** : touch targets 48px, contrast 4.5:1, ARIA labels
- **Family-friendly** : pas de jargon, boutons avec labels, facile à annuler
- **Progressive disclosure** : minimum visible, détails on demand

---

## Specs clés (décisions prises)

| Sujet | Décision |
|---|---|
| Auth | Magic link email uniquement |
| Rôles | Admin + membre |
| Invitations | Par lien unique + par email |
| Types événements | Prédéfinis (Vacances, Dispo, Voyage) + custom |
| Granularité | Journée entière OU créneau horaire |
| Lieu | Texte libre (pas Google Maps) |
| Vue calendrier | Vue mois |
| Couleurs membres | Automatiques (10 couleurs) |
| Filtres membres | Oui (cocher/décocher) |
| Vie privée | Événements privés → "Occupé" dans le groupe |
| Accès groupe | Strictement privé |
| Social | Aucune feature sociale |
| Style | Material Design, light mode only |
| Langues | FR + EN |
| Multi-groupes | Illimité |
| Admin quitte | Transfert auto au plus ancien membre |

---

## Features POST-V1 (ne PAS implémenter maintenant)

- Événements récurrents
- Statut tentatif/confirmé
- Import/export iCal + synchro Google Calendar
- Détection chevauchements + suggestions créneaux communs
- Notifications push
- Mode offline
- Dark mode

---

## Deps (package.json)

### Production
```
next: 16.2.1
react: 19.2.4
@mui/material: ^7.3.9
@mui/icons-material: ^7.3.9
@emotion/react: ^11.14.0
@emotion/styled: ^11.14.1
@fullcalendar/core: ^6.1.20
@fullcalendar/daygrid: ^6.1.20
@fullcalendar/interaction: ^6.1.20
@fullcalendar/react: ^6.1.20
@supabase/ssr: ^0.9.0
@supabase/supabase-js: ^2.99.3
next-intl: ^4.8.3
```

### Dev
```
typescript: ^5
@types/react: ^19
eslint: ^9
eslint-config-next: 16.2.1
tailwindcss: ^4
@tailwindcss/postcss: ^4
```

---

## Traductions (i18n)

### Clés existantes (FR)
```json
{
  "common": {
    "appName": "Together",
    "loading": "Chargement...",
    "save": "Enregistrer",
    "cancel": "Annuler",
    "delete": "Supprimer",
    "edit": "Modifier",
    "create": "Créer",
    "back": "Retour",
    "confirm": "Confirmer",
    "error": "Une erreur est survenue",
    "success": "Opération réussie"
  },
  "landing": {
    "title": "Together",
    "subtitle": "Synchronisez vos calendriers en famille, simplement.",
    "cta": "Se connecter avec un email",
    "step1Title": "Créez votre groupe",
    "step1Desc": "Rassemblez votre famille en un clic",
    "step2Title": "Ajoutez vos vacances",
    "step2Desc": "Indiquez vos disponibilités et vos projets",
    "step3Title": "Voyez qui est dispo",
    "step3Desc": "Un calendrier partagé pour toute la famille"
  },
  "auth": {
    "loginTitle": "Connexion",
    "loginSubtitle": "Entrez votre email pour recevoir un lien de connexion",
    "emailLabel": "Adresse email",
    "emailPlaceholder": "votre@email.com",
    "sendLink": "Envoyer le lien magique",
    "linkSent": "Lien envoyé !",
    "linkSentDesc": "Vérifiez votre boîte mail et cliquez sur le lien pour vous connecter.",
    "checkSpam": "Pensez à vérifier vos spams.",
    "invalidEmail": "Adresse email invalide",
    "logout": "Déconnexion"
  },
  "profile": {
    "title": "Mon profil",
    "displayName": "Nom d'affichage",
    "displayNamePlaceholder": "Comment vous appelle votre famille ?",
    "language": "Langue",
    "saved": "Profil enregistré",
    "avatarAlt": "Photo de profil"
  },
  "dashboard": {
    "greeting": "Bonjour, {name}",
    "myGroups": "Mes groupes",
    "createGroup": "Créer un groupe",
    "noGroups": "Vous n'avez pas encore de groupe",
    "noGroupsHint": "Créez votre premier groupe pour commencer !",
    "upcomingEvents": "Prochains événements",
    "noEvents": "Aucun événement à venir",
    "members": "{count, plural, =1 {1 membre} other {# membres}}"
  },
  "nav": {
    "calendar": "Calendrier",
    "groups": "Groupes",
    "profile": "Profil"
  }
}
```

---

## Code source complet des fichiers clés

### `src/proxy.ts` (Middleware)
```typescript
import createMiddleware from 'next-intl/middleware';
import { NextRequest } from 'next/server';
import { routing } from '@/lib/i18n/routing';
import { updateSession } from '@/lib/supabase/middleware';

const intlMiddleware = createMiddleware(routing);

export async function proxy(request: NextRequest) {
  const supabaseResponse = await updateSession(request);
  const intlResponse = intlMiddleware(request);
  if (intlResponse) {
    supabaseResponse.cookies.getAll().forEach((cookie) => {
      intlResponse.cookies.set(cookie.name, cookie.value);
    });
    return intlResponse;
  }
  return supabaseResponse;
}

export const config = {
  matcher: ['/', '/(fr|en)/:path*'],
};
```

### `src/lib/supabase/server.ts`
```typescript
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Called from Server Component — middleware handles refresh
          }
        },
      },
    }
  );
}
```

### `src/lib/supabase/middleware.ts`
```typescript
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return request.cookies.getAll(); },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );
  await supabase.auth.getUser();
  return supabaseResponse;
}
```

### `src/app/[locale]/auth/callback/route.ts`
```typescript
import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? '/dashboard';

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        const { data: profile } = await supabase
          .from('profiles').select('id').eq('id', user.id).single();
        if (!profile) {
          await supabase.from('profiles').insert({
            id: user.id,
            display_name: user.email?.split('@')[0] ?? 'User',
            preferred_locale: 'fr',
          });
        }
      }
      return NextResponse.redirect(`${origin}/fr${next}`);
    }
  }
  return NextResponse.redirect(`${origin}/fr/login?error=auth`);
}
```

---

## Wireframes (ASCII) des écrans principaux

### Landing (`/`)
```
┌─────────────────────────────────┐
│     [Calendar icon]             │
│     Together                    │
│     Synchronisez vos calendriers│
│     [Se connecter avec email]   │
│     [Card 1] [Card 2] [Card 3] │
└─────────────────────────────────┘
```

### Dashboard (`/dashboard`)
```
┌─────────────────────────────────┐
│  Together              [EN]     │  ← TopBar
├─────────────────────────────────┤
│  Bonjour, Thomas                │
│  Mes groupes                    │
│  ┌ Famille Dupont           > ┐ │
│  └────────────────────────────┘ │
│  [+ Créer un groupe]            │
├─────────────────────────────────┤
│  [Calendrier] [Groupes] [Profil]│  ← BottomNav
└─────────────────────────────────┘
```

### Calendrier de groupe (Milestone 4)
```
┌─────────────────────────────────┐
│  ← Famille Dupont      [gear]  │
├─────────────────────────────────┤
│  Filtres:                       │
│  [Blue Thomas] [Red Marie]      │
│  [Green Lucas] [Purple Emma]    │
├─────────────────────────────────┤
│       < Août 2026 >            │
│  Lu Ma Me Je Ve Sa Di           │
│  Blue Vacances Bretagne ─────   │
│  Red  Occupé ────────────────   │
│  Green Dispo weekend ──  ──     │
│  Purple Voyage Espagne ──────   │
├─────────────────────────────────┤
│  [Calendrier] [Groupes] [Profil]│
└─────────────────────────────────┘
```

---

## Agents (personnalités pour multi-agent)

4 agents définis dans `together/agents/` :

1. **Expert Architect** (blue) : Schema Supabase, RLS, structure Next.js, perf
2. **Spec Master** (orange) : Specs, user stories, acceptance criteria, anti-scope-creep
3. **UI/UX Expert** (purple) : Design system, wireframes, accessibilité, mobile-first
4. **QA Tester** (red) : Tests fonctionnels, cross-device, i18n, sécurité, edge cases

---

## Points d'attention / Notes

1. **AGENTS.md** dans `app/` dit : "This is NOT the Next.js you know" — lire `node_modules/next/dist/docs/` avant de coder pour vérifier les APIs Next.js 16
2. **Middleware** : le fichier s'appelle `proxy.ts` (pas `middleware.ts`) et exporte `proxy` (pas `middleware`)
3. **Auth callback** redirige hardcodé vers `/fr/dashboard` — devrait utiliser la locale du user
4. Le **dashboard** fetch les groupes via une jointure `group_members` → `groups` avec la syntaxe Supabase `select('group_id, role, groups(id, name, description)')`
5. **MUI v7** (pas v5 comme dans le PLAN.md initial) — le package.json a `@mui/material: ^7.3.9`
6. **Next.js 16** (pas 14 comme dans le PLAN.md) — `next: 16.2.1`
7. **React 19** — `react: 19.2.4`
8. Les pages **Calendar** et **Groups** (Milestone 2-4) n'existent pas encore — les liens du BottomNav pointent vers `/calendar` et `/groups/new` qui ne sont pas implémentés

---

## Prochaines étapes recommandées

1. Finir Milestone 1 : vérifier build, tester auth flow complet
2. Milestone 2 : Implémenter les groupes
   - Page création de groupe (`/groups/new`)
   - Page groupe avec membres (`/groups/[groupId]`)
   - Système d'invitation (lien + email)
   - Gestion rôles admin/membre
3. Milestone 3 : Calendrier perso avec FullCalendar
4. Milestone 4 : Calendrier de groupe agrégé
5. Milestone 5 : Polish, dashboard enrichi, responsive vérifié
