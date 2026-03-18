#!/usr/bin/env python3
"""
The Wisdom Engine — Premier Prototype
Un jeu textuel où 3 agents philosophiques guident le joueur
à travers la mission "The Invisible Hand" à Venise.
"""

import json
import os
import sys
import textwrap

# ─── Couleurs terminal ───────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
WHITE = "\033[97m"


def wrap(text, width=72):
    return "\n".join(textwrap.fill(line, width) for line in text.splitlines())


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n{DIM}[Appuie sur Entrée pour continuer]{RESET}")


def print_header(title):
    print(f"\n{BOLD}{CYAN}{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}{RESET}\n")


def print_agent(name, color, text):
    print(f"{BOLD}{color}  [{name}]{RESET}")
    print(f"{color}  {wrap(text)}{RESET}\n")


# ─── Agents philosophiques ────────────────────────────────────────────

AGENTS = {
    "taoisme": {
        "name": "Laozi",
        "color": GREEN,
        "philosophy": "Wu Wei — agir sans forcer",
        "icon": "☯",
    },
    "stoicisme": {
        "name": "Marc Aurèle",
        "color": BLUE,
        "philosophy": "Contrôle seulement ce qui dépend de toi",
        "icon": "⚖",
    },
    "existentialisme": {
        "name": "Simone de Beauvoir",
        "color": MAGENTA,
        "philosophy": "L'existence précède l'essence — choisis librement",
        "icon": "✦",
    },
}


# ─── Profil joueur ───────────────────────────────────────────────────

def make_profile():
    return {
        "taoisme": 0,
        "stoicisme": 0,
        "existentialisme": 0,
        "confucianisme": 0,
        "soufisme": 0,
        "zen": 0,
    }


def print_radar(profile):
    """Affiche un spider chart ASCII simple."""
    print(f"\n{BOLD}{WHITE}  ╔══ Profil Philosophique ══╗{RESET}")
    max_val = max(max(profile.values()), 1)
    for axis, val in profile.items():
        bar_len = int((val / max(max_val, 5)) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        label = axis.capitalize().ljust(18)
        print(f"  {DIM}│{RESET} {label} {YELLOW}{bar}{RESET} {val}")
    print(f"  {BOLD}{WHITE}╚{'═' * 28}╝{RESET}")


# ─── Scénarios ────────────────────────────────────────────────────────

SCENARIO = {
    "title": "The Invisible Hand",
    "lieu": "Venise, 1486",
    "intro": (
        "Venise brille sous le soleil. Le Doge Marco Barbarigo règne par "
        "la corruption : taxes écrasantes, espions dans chaque quartier, "
        "et une alliance secrète avec les Templiers.\n\n"
        "Tu es un Assassin envoyé pour libérer la ville. Mais comment ?"
    ),
    "phases": [
        {
            "id": "approach",
            "title": "Acte I — L'Approche",
            "situation": (
                "Tu arrives à Venise par bateau. Le port grouille de gardes. "
                "Un contact t'attend dans une taverne, mais tu as aussi repéré "
                "un marchand mécontent et un prêtre qui prêche contre le Doge."
            ),
            "agents_speak": {
                "taoisme": (
                    "L'eau ne force pas son chemin à travers la pierre — "
                    "elle la contourne. Observe d'abord. Les courants de "
                    "mécontentement existent déjà. Laisse-les te guider."
                ),
                "stoicisme": (
                    "Tu ne contrôles pas la ville, ni le Doge, ni les gardes. "
                    "Tu contrôles seulement tes choix. Que peux-tu faire "
                    "maintenant, avec vertu, sans dépendre du résultat ?"
                ),
                "existentialisme": (
                    "Personne ne t'a assigné un destin. Tu es libre de choisir "
                    "ton approche. Mais souviens-toi : chaque choix te définit. "
                    "Il n'y a pas de 'bonne réponse' — il y a TA réponse."
                ),
            },
            "choices": [
                {
                    "text": "Observer la ville pendant 3 jours sans agir",
                    "effects": {"taoisme": 3, "zen": 1},
                    "result": (
                        "Pendant trois jours, tu observes les flux de la ville. "
                        "Tu découvres les réseaux de corruption, les points "
                        "faibles, et surtout — le mécontentement profond du peuple. "
                        "Tu as une carte mentale complète de Venise."
                    ),
                },
                {
                    "text": "Aller directement au contact dans la taverne",
                    "effects": {"stoicisme": 2, "confucianisme": 1},
                    "result": (
                        "Ton contact, Antonio, est un marchand ruiné par le Doge. "
                        "Il te donne des informations clés et te présente un réseau "
                        "de résistants. Tu as des alliés, mais tu dépends d'eux."
                    ),
                },
                {
                    "text": "Approcher le marchand ET le prêtre — forger ta propre voie",
                    "effects": {"existentialisme": 3, "soufisme": 1},
                    "result": (
                        "Tu crées tes propres alliances, hors des sentiers battus. "
                        "Le marchand veut la justice économique. Le prêtre veut la "
                        "justice morale. Ensemble, ils représentent la voix du peuple."
                    ),
                },
            ],
        },
        {
            "id": "plan",
            "title": "Acte II — Le Plan",
            "situation": (
                "Tu as compris la situation. Le Doge organise un grand bal "
                "dans 5 jours. C'est une opportunité. Mais le bal est "
                "aussi un piège — le Doge soupçonne un complot.\n\n"
                "Comment veux-tu agir ?"
            ),
            "agents_speak": {
                "taoisme": (
                    "Le roseau plie mais ne rompt pas. N'attaque pas le Doge "
                    "de front. Modifie les conditions autour de lui : ses "
                    "alliés, ses finances, sa réputation. Le système fera "
                    "le reste."
                ),
                "stoicisme": (
                    "Prépare-toi au pire. Si le plan échoue, que feras-tu ? "
                    "La vertu n'est pas dans le succès, mais dans l'intention "
                    "juste. Agis selon tes principes, quel que soit le résultat."
                ),
                "existentialisme": (
                    "Ce bal est un théâtre. Tout le monde y joue un rôle. "
                    "Toi seul peux choisir de ne PAS jouer le jeu — ou de "
                    "le renverser complètement. L'absurde est ta liberté."
                ),
            },
            "choices": [
                {
                    "text": "Saboter les finances du Doge — couper ses soutiens",
                    "effects": {"taoisme": 3, "confucianisme": 2},
                    "result": (
                        "Tu détournes les livraisons d'or, révèles les comptes "
                        "secrets. Les marchands retournent leur veste. Le Doge "
                        "perd ses alliés un par un — comme un arbre dont on "
                        "coupe les racines. Il ne le sait pas encore."
                    ),
                },
                {
                    "text": "Infiltrer le bal et assassiner le Doge",
                    "effects": {"stoicisme": 2, "existentialisme": 2},
                    "result": (
                        "Le chemin direct. Tu t'entraînes, tu te prépares. "
                        "Tu acceptes que tu pourrais mourir. C'est un choix "
                        "radical, irréversible, mais clair. Ton destin est "
                        "entre tes mains."
                    ),
                },
                {
                    "text": "Utiliser le bal pour retourner le peuple contre le Doge",
                    "effects": {"existentialisme": 2, "soufisme": 2, "confucianisme": 1},
                    "result": (
                        "Tu orchestres une révélation publique. Au milieu du bal, "
                        "les preuves de corruption éclatent. Le peuple se soulève "
                        "— non pas parce que tu l'as forcé, mais parce qu'il a "
                        "enfin vu la vérité."
                    ),
                },
            ],
        },
        {
            "id": "climax",
            "title": "Acte III — La Chute du Doge",
            "situation": (
                "Le moment décisif approche. Le Doge est affaibli mais "
                "dangereux. Il a découvert qu'un complot existe. Ses gardes "
                "sont en alerte maximale.\n\n"
                "Comment achèves-tu ta mission ?"
            ),
            "agents_speak": {
                "taoisme": (
                    "L'eau qui a creusé la montagne n'a jamais frappé la "
                    "pierre — elle a simplement coulé. Le Doge est déjà tombé. "
                    "Il ne le sait pas encore. Laisse la gravité faire."
                ),
                "stoicisme": (
                    "Quoi qu'il arrive maintenant, tu as agi avec vertu. "
                    "Le résultat n'est pas entre tes mains. Fais ce qui est "
                    "juste et accepte les conséquences avec dignité."
                ),
                "existentialisme": (
                    "C'est ici que tout se joue. Il n'y a pas de filet. "
                    "Pas de destin. Pas d'excuse. Ton choix final te définira "
                    "à jamais. Choisis en conscience."
                ),
            },
            "choices": [
                {
                    "text": "Ne rien faire — le système s'effondre de lui-même",
                    "effects": {"taoisme": 5, "zen": 2},
                    "result": (
                        "Tu restes dans l'ombre. Les alliés du Doge l'abandonnent. "
                        "Le peuple refuse de lui obéir. Les gardes déposent les "
                        "armes. Le Doge tombe — sans qu'une seule lame soit tirée.\n\n"
                        "C'est la voie du Wu Wei : l'action par la non-action."
                    ),
                },
                {
                    "text": "Affronter le Doge en face à face, avec honneur",
                    "effects": {"stoicisme": 4, "existentialisme": 2},
                    "result": (
                        "Tu te présentes devant le Doge. Seul. Tu lui offres "
                        "le choix : abdiquer ou combattre. Il choisit le combat.\n\n"
                        "Le duel est bref. Tu gagnes — mais tu lui accordes la "
                        "dignité d'une fin honorable. La vertu dans la victoire."
                    ),
                },
                {
                    "text": "Disparaître — laisser Venise écrire sa propre histoire",
                    "effects": {"existentialisme": 4, "soufisme": 3},
                    "result": (
                        "Tu quittes Venise. Le peuple, éveillé, fait sa propre "
                        "révolution. Tu ne seras jamais crédité. Tu ne seras "
                        "jamais connu.\n\n"
                        "Mais Venise est libre — et cette liberté leur appartient, "
                        "pas à toi. C'est le plus grand cadeau que tu pouvais faire."
                    ),
                },
            ],
        },
    ],
}


# ─── Boucle de jeu ───────────────────────────────────────────────────

def play():
    profile = make_profile()

    clear()
    print(f"""
{BOLD}{CYAN}
  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║          T H E   W I S D O M   E N G I N E       ║
  ║                                                  ║
  ║          Premier Prototype — Venise 1486         ║
  ║                                                  ║
  ╚══════════════════════════════════════════════════╝
{RESET}""")

    print(f"  {DIM}3 agents philosophiques te guideront.{RESET}")
    print(f"  {DIM}Tes choix façonnent ton profil de sagesse.{RESET}")
    print()

    # Présenter les agents
    for key, agent in AGENTS.items():
        icon = agent["icon"]
        name = agent["name"]
        phil = agent["philosophy"]
        color = agent["color"]
        print(f"  {color}{BOLD}{icon} {name}{RESET} {DIM}— {phil}{RESET}")

    pause()

    # Intro du scénario
    clear()
    print_header(f"Mission : {SCENARIO['title']}")
    print(f"  {BOLD}{YELLOW}{SCENARIO['lieu']}{RESET}\n")
    print(f"  {wrap(SCENARIO['intro'])}")
    pause()

    # Phases de jeu
    for phase in SCENARIO["phases"]:
        clear()
        print_header(phase["title"])
        print(f"  {wrap(phase['situation'])}")
        print()

        # Les agents parlent
        print(f"  {DIM}{'─' * 50}{RESET}")
        print(f"  {BOLD}{WHITE}Les sages te conseillent :{RESET}\n")

        for agent_key, text in phase["agents_speak"].items():
            agent = AGENTS[agent_key]
            print_agent(
                f"{agent['icon']} {agent['name']}",
                agent["color"],
                text,
            )

        print(f"  {DIM}{'─' * 50}{RESET}")
        print(f"\n  {BOLD}{WHITE}Que fais-tu ?{RESET}\n")

        for i, choice in enumerate(phase["choices"], 1):
            print(f"  {BOLD}{YELLOW}  [{i}]{RESET} {choice['text']}")

        print()

        # Input joueur
        while True:
            try:
                raw = input(f"  {BOLD}> {RESET}")
                idx = int(raw) - 1
                if 0 <= idx < len(phase["choices"]):
                    break
            except (ValueError, EOFError):
                pass
            print(f"  {RED}Choisis 1, 2 ou 3.{RESET}")

        chosen = phase["choices"][idx]

        # Appliquer les effets
        for axis, pts in chosen["effects"].items():
            profile[axis] = profile.get(axis, 0) + pts

        print(f"\n  {GREEN}{wrap(chosen['result'])}{RESET}")

        # Afficher le radar
        print_radar(profile)
        pause()

    # ─── Fin de partie ─────────────────────────────────────────────
    clear()
    print_header("Fin de la Mission")

    # Déterminer la philosophie dominante
    dominant = max(profile, key=profile.get)
    dominant_label = dominant.capitalize()
    dominant_score = profile[dominant]

    print(f"  {BOLD}{WHITE}Mission accomplie. Venise est transformée.{RESET}\n")
    print(f"  Ta voie dominante : {BOLD}{YELLOW}{dominant_label}{RESET} ({dominant_score} pts)\n")

    endings = {
        "taoisme": (
            "Tu as suivi la voie du Wu Wei. Sans forcer, tu as laissé les "
            "systèmes se transformer d'eux-mêmes. La sagesse n'est pas dans "
            "l'action — mais dans la compréhension du moment juste."
        ),
        "stoicisme": (
            "Tu as agi avec vertu, sans te soucier du résultat. Marc Aurèle "
            "serait fier : tu as contrôlé ce qui dépendait de toi et accepté "
            "le reste avec sérénité."
        ),
        "existentialisme": (
            "Tu as choisi librement, en assumant chaque conséquence. Beauvoir "
            "dirait que tu as créé ton essence par tes actes. Ta liberté a "
            "donné la liberté aux autres."
        ),
        "confucianisme": (
            "Tu as agi avec responsabilité sociale. Tes alliances et ton sens "
            "du devoir collectif ont transformé la ville de l'intérieur."
        ),
        "soufisme": (
            "Tu t'es transformé toi-même avant de transformer le monde. "
            "La vérité intérieure a rayonné vers l'extérieur."
        ),
        "zen": (
            "Dans le silence et l'attention, tu as trouvé la clarté. "
            "Chaque geste était précis, chaque instant vécu pleinement."
        ),
    }

    ending = endings.get(dominant, endings["taoisme"])
    print(f"  {wrap(ending)}\n")

    print_radar(profile)

    print(f"\n  {DIM}{'─' * 50}{RESET}")
    print(f"  {DIM}The Wisdom Engine — Prototype v0.1{RESET}")
    print(f"  {DIM}12 agents prévus. 3 actifs dans ce proto.{RESET}")
    print(f"  {DIM}Prochaine étape : agents IA dynamiques (Claude API){RESET}")
    print()


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}À bientôt, Assassin.{RESET}\n")
        sys.exit(0)
