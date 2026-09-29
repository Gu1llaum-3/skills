"""Tests de l'extraction de build_skills_page.py.

Usage : python3 -m unittest docs/test_build_skills_page.py (depuis la racine du dépôt)
"""
import sys, tempfile, textwrap, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_skills_page as b


def write_skill(root, name, body, user=False, desc="Fait une chose."):
    d = Path(root) / name
    d.mkdir()
    flag = "disable-model-invocation: true\n" if user else ""
    (d / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "{desc}"\n{flag}---\n\n' + textwrap.dedent(body))


class Extraction(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_ac2_famille_lue_dans_le_frontmatter(self):
        write_skill(self.root, "feature", "Corps.", user=True, desc="Cadrer une idée.")
        write_skill(self.root, "plan", "Corps.")
        skills = b.load_skills(self.root)
        self.assertEqual(skills["feature"]["user"], True)
        self.assertEqual(skills["plan"]["user"], False)
        self.assertEqual(skills["feature"]["desc"], "Cadrer une idée.")

    def test_ac2_appels_meme_coupes_par_un_retour_a_la_ligne(self):
        write_skill(self.root, "interview", """\
            Appeler le Skill
            tool avec « domain-modeling » dès le début. Puis appeler le Skill tool avec
            « research » si besoin, et encore le Skill tool avec « research ».
            """)
        write_skill(self.root, "domain-modeling", "Corps.")
        write_skill(self.root, "research", "Corps.")
        self.assertEqual(b.load_skills(self.root)["interview"]["calls"],
                         ["domain-modeling", "research"])

    def test_ac3_appel_vers_un_skill_absent_ignore(self):
        write_skill(self.root, "plan", "Appeler le Skill tool avec « code-review ».")
        self.assertEqual(b.load_skills(self.root)["plan"]["calls"], [])

    def test_ac1_page_generee_avec_les_donnees_a_la_place_du_marqueur(self):
        write_skill(self.root, "plan", "Corps.", desc="Planifier.")
        html = b.build_page(self.root, "<script>const DATA = /*DATA*/;</script>")
        self.assertNotIn("/*DATA*/", html)
        self.assertIn('"plan": {"desc": "Planifier."', html)
        self.assertIn('"situations": []', html)

    def test_ac3_situations_lues_dans_la_carte_de_next(self):
        write_skill(self.root, "plan", "Corps.")
        write_skill(self.root, "next", """\
            ## 2. La carte

            | Situation | Skill |
            |---|---|
            | Tout est décidé, ça tient en une session | `/plan` |
            | Un ticket à analyser avant de coder | `/plan <ticket>` |
            | Un nom à trouver | `/naming` |

            Le parcours principal : `/feature` → `/plan`.
            """, user=True)
        self.assertEqual(b.load_situations(self.root), [
            {"q": "Tout est décidé, ça tient en une session", "s": "plan", "cmd": "/plan"},
            {"q": "Un ticket à analyser avant de coder", "s": "plan", "cmd": "/plan <ticket>"},
        ])

    def test_ac3_skill_sans_groupe_range_dans_autres_selon_sa_famille(self):
        write_skill(self.root, "plan", "Corps.")
        write_skill(self.root, "atelier", "Corps.", user=True)
        write_skill(self.root, "relire", "Corps.")
        template = """const COLUMNS = [
          { title: "Toi seul", groups: [
            ["Cadrer", ["feature"]],
          ]},
          { title: "Le parcours", groups: [
            ["Construire", ["plan", "implement"]],
          ]},
        ];
        const DATA = /*DATA*/;"""
        self.assertIn('"others": {"u": ["atelier"], "m": ["relire"]}',
                      b.build_page(self.root, template))


class DepotReel(unittest.TestCase):
    def test_ac3_chaque_skill_du_depot_a_un_groupe_sur_la_carte(self):
        template = (b.ROOT / "docs" / "skills.template.html").read_text()
        self.assertEqual(b.ungrouped(b.load_skills(b.ROOT), template), {"u": [], "m": []})

    def test_ac2_interview_appelle_domain_modeling(self):
        skills = b.load_skills(b.ROOT)
        self.assertEqual(skills["interview"]["calls"], ["domain-modeling", "research", "adr"])
        self.assertEqual(sorted(skills["implement"]["calls"]),
                         ["adr", "plan", "review", "tdd", "tickets"])


if __name__ == "__main__":
    unittest.main()
