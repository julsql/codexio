from datetime import date
from decimal import Decimal

from main.core.domain import Album

# ASTÉRIX

# ISBN et URLs
ASTERIX_ISBN = 9782864976165
ASTERIX_URLS = {
    'BDPHILE': "https://www.bdphile.fr/album/view/160391/",
    'BDGEST': "https://www.bedetheque.com/BD-Asterix-Hors-Serie-C14-L-Empire-du-Milieu-467639.html",
    'BDFUGUE': "https://www.bdfugue.com/catalogsearch/result/?q=9782864976165"
}

# Données par source
ASTERIX_DATA = {
    'BDPHILE': Album(isbn=9782864976165,
                     title="L'empire du milieu",
                     series="Astérix (Albums des films)",
                     number="10",
                     writer="Olivier Gay",
                     illustrator="Fabrice Tarrin",
                     colorist="Thierry Mébarki",
                     publisher="Albert René",
                     edition="Édition originale Noté : Impression en décembre 2022 - n° 616-5-01 Impression et reliure par Pollina - n°13651",
                     publication_date=date(2023, 2, 8),
                     number_of_pages=48,
                     purchase_price=Decimal('10.5'),
                     synopsis="Nous sommes en 50 av J.-C. Loin, très loin du petit village d'Armorique que nous connaissons bien,"
                              " l'Impératrice de Chine est emprisonnée suite à coup d'état fomenté par l'infâme Deng Tsin Qin."
                              "<br/>La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa fidèle guerrière Tat Han et"
                              " Graindemaïs, le neveu du marchand phénicien Epidemaïs, s'enfuit pour demander de l'aide aux"
                              " Irréductibles Gaulois.",
                     image="https://static.bdphile.fr/images/media/cover/0160/160391.jpg"
                     ),
    'BDGEST': Album(isbn=9782864976165,
                    title="L'Empire du Milieu",
                    series="Astérix (Hors Série)",
                    number="C14",
                    writer="Olivier Gay",
                    illustrator="Fabrice Tarrin",
                    colorist="Thierry Mébarki",
                    publisher="Les Éditions Albert René",
                    publication_date=date(2023, 2, 8),
                    number_of_pages=44,
                    purchase_price=Decimal('10.90'),
                    synopsis='Nous sommes en 50 av J.-C. Loin, très loin du petit village '
                             "d'Armorique que nous connaissons bien, l'Impératrice de Chine "
                             "est emprisonnée suite à un coup d'état fomenté par l'infâme Deng "
                             "Tsin Qin. La princesse Fu Yi, fille unique de l'Impératrice, "
                             'aidée par sa fidèle guerrière Tat Han et Graindemaïs, le neveu '
                             "du marchand phénicien Épidemaïs, s'enfuit pour demander de "
                             "l'aide aux Irréductibles Gaulois.<br />\n"
                             '<br />\n'
                             'Une histoire originale basée sur le scénario du film Astérix '
                             "&amp; Obélix, L'Empire du Milieu réalisé par Guillaume Canet.",
                    image="https://www.bedetheque.com/media/Couvertures/Couv_467639.jpg"
                    ),
    'BDFUGUE': Album(isbn=9782864976165,
                     title="L'empire du milieu (album illustré)",
                     series="Astérix",
                     number="1",
                     writer="Olivier Gay",
                     illustrator="Fabrice Tarrin",
                     publisher="ALBERT RENE",
                     publication_date=date(2023, 2, 8),
                     number_of_pages=48,
                     purchase_price=Decimal('10.90'),
                     synopsis='NOUVEL ALBUM ILLUSTRÉ   Nous sommes en 50 av J.-C. Loin, très '
                              "loin du petit village d'Armorique que nous connaissons bien, "
                              "l'Impératrice de Chine est emprisonnée suite à coup d'état "
                              "fomenté par l'infâme Deng Tsin Qin.  \r\n"
                              '\r\n'
                              "La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa "
                              'fidèle guerrière Tat Han et Graindemaïs, le neveu du marchand '
                              "phénicien Epidemaïs, s'enfuit pour demander de l'aide aux "
                              'Irréductibles Gaulois.\r\n'
                              '\r\n'
                              'Une histoire originale basée sur le scénario du film Astérix & '
                              "Obélix, L'Empire du Milieu réalisé par Guillaume Canet.",
                     image="https://www.bdfugue.com/media/catalog/product/cache/0d950bd4d3aaddc02a824ea154d9c41e/9/7/9782864976165_1_75.jpg"
                     )
}

# SAMBRE

SAMBRE_ISBN = 9782754801096

# Données par source

SAMBRE_DATA = {
    'BDPHILE': Album(
        isbn=SAMBRE_ISBN,
        title="Hiver 1831 - La Lune qui regarde",
        series="La Guerre des Sambre - Hugo & Iris",
        number="3",
        writer="Yslaire (Bernard Hislaire)",
        illustrator="Jean Bastide,Vincent Mézil",
        publisher="Futuropolis - Glénat",
        edition="1 réédition",
        publication_date=date(2009, 11, 25),
        number_of_pages=56,
        purchase_price=Decimal('14.00'),
        synopsis='Hiver 1831. À la Bastide, la mort des parents Sambre laisse une '
                 "maison vide et ses occupants solitaires. Blanche, l'épouse "
                 "délaissée, s'échappe de cette atmosphère pesante en compagnie "
                 "d'un \x93 cousin \x94 plus joyeux. Les sœurs d'Hugo portent le "
                 "deuil dans un silence réprobateur. Hugo Sambre s'occupe pour la "
                 'première fois de sa fille Sarah, en lui faisant la lecture du '
                 "manuscrit de La guerre des yeux. L'annonce du retour d'Iris à "
                 "Paris, l'actrice aux yeux rouges qui l'a envoûté, décide Hugo à "
                 "quitter précipitamment la Bastide, dans l'espoir de la retrouver",
        image="https://static.bdphile.fr/images/media/cover/0005/5175.jpg"
    ),
    'BDGEST': Album(
        isbn=SAMBRE_ISBN,
        title="Chapitre 3 - Hiver 1831 : la lune qui regarde",
        series="La guerre des Sambre - Hugo & Iris",
        number="3",
        writer="Yslaire",
        illustrator="Jean Bastide,Vincent Mézil",
        colorist="Jean Bastide,Vincent Mézil",
        publisher="Futuropolis / Glénat",
        publication_date=date(2009, 11, 25),
        number_of_pages=56,
        purchase_price=Decimal('15.50'),
        synopsis="Avec Hugo et Iris, Yslaire, revient sur la jeunesse d'Hugo "
                 "Sambre, le père de Bernard Sambre, sur l'écriture de son "
                 'manuscrit La guerre des yeux, sur sa passion funeste pour Iris, '
                 'mère de Julie, qui le mène au suicide. Ce troisième tome clôt de '
                 'façon magistrale ce premier cycle de La Guerre des Sambre !<br '
                 '/>\n'
                 'Hiver 1931. À la Bastide, la mort des parents Sambre laisse une '
                 "maison vide et ses occupants solitaires. Blanche, l'épouse "
                 "délaissée, s'échappe de cette atmosphère pesante en compagnie "
                 "d'un 'cousin' plus joyeux. Les soeurs d'Hugo portent le deuil "
                 "dans un silence réprobateur. Hugo Sambre s'occupe pour la "
                 'première fois de sa fille Sarah, en lui faisant la lecture du '
                 "manuscrit de La guerre des yeux. L'annonce du retour d'Iris à "
                 "Paris, l'actrice aux yeux rouges qui l'a envoûté, décide Hugo à "
                 'quitter précipitamment la Bastide, dans l?espoir de la '
                 'retrouver?<br />\n',
        image="https://www.bedetheque.com/media/Couvertures/Couv_98900.jpg"
    ),
    'BDFUGUE': Album(
        isbn=SAMBRE_ISBN,
        title="hiver 1931",
        series="La guerre des sambre - Hugo et Iris",
        number="3",
        writer="Yslaire",
        illustrator="Jean Bastide,Vincent Mézil",
        colorist="Jean Bastide,Vincent Mézil",
        publisher="GLENAT",
        publication_date=date(2009, 11, 25),
        number_of_pages=58,
        purchase_price=Decimal('13.90'),
        synopsis="Avec Hugo et Iris, Yslaire, revient sur la jeunesse d'Hugo "
                 "Sambre, le père de Bernard Sambre, sur l'écriture de son "
                 'manuscrit La guerre des yeux, sur sa passion funeste pour Iris, '
                 'mère de Julie, qui le mène au suicide. Ce troisième tome clôt de '
                 'façon magistrale ce premier cycle de La Guerre des Sambre !\r\n'
                 'Hiver 1931. À la Bastide, la mort des parents Sambre laisse une '
                 "maison vide et ses occupants solitaires. Blanche, l'épouse "
                 "délaissée, s'échappe de cette atmosphère pesante en compagnie "
                 "d'un « cousin » plus joyeux. Les soeurs d'Hugo portent le deuil "
                 "dans un silence réprobateur. Hugo Sambre s'occupe pour la "
                 'première fois de sa fille Sarah, en lui faisant la lecture du '
                 "manuscrit de La guerre des yeux. L'annonce du retour d'Iris à "
                 "Paris, l'actrice aux yeux rouges qui l'a envoûté, décide Hugo à "
                 "quitter précipitamment la Bastide, dans l'espoir de la "
                 'retrouver...',
        image="https://www.bdfugue.com/media/catalog/product/cache/0d950bd4d3aaddc02a824ea154d9c41e/9/7/9782754801096_1_75.jpg"
    )
}

# THORGAL

THORGAL_ISBN = 9782803603589

# Données par source

THORGAL_DATA = {
    'BDPHILE': Album(
        isbn=THORGAL_ISBN,
        title="La Magicienne trahie",
        series="Thorgal",
        number="1",
        writer="Jean Van Hamme",
        illustrator="Grzegorz Rosinski",
        publisher="Le Lombard",
        edition='Édition originale - 18 rééditions Les 2 premiers tomes sont parus en même temps. Tome 3 à paraître au 4e plat',
        publication_date=date(1980, 1, 1),
        number_of_pages=48,
        purchase_price=Decimal('10.00'),
        synopsis='Prise dans une tempête en pleine mer, une expédition Viking '
                 "découvre un bébé dans une mystérieuse embarcation. L'enfant est "
                 "baptisé du nom de Thorgal. Prodige du tir à l'arc, épris de "
                 "liberté et de justice, il n'aura de cesse de défendre les siens "
                 "et d'aspirer à une vie paisible. Son histoire est celle d'un "
                 "homme que les Dieux ont décidé de mettre à l'épreuve et qui "
                 'percera, au fil de ses aventures, le mystère de ses origines.',
        image="https://static.bdphile.fr/images/media/cover/0098/98648.jpg"
    ),
    'BDGEST': Album(
        isbn=THORGAL_ISBN,
        title="La Magicienne trahie",
        series="Thorgal",
        number="1",
        writer="Jean Van Hamme",
        illustrator="Grzegorz Rosinski",
        colorist="<Quadrichromie>",
        publisher="Lombard",
        publication_date=date(1980, 1, 1),
        number_of_pages=46,
        purchase_price=Decimal('13.95'),
        synopsis='Prépublication dans Tintin édition française n° 106, 107, 116, '
                 '129, 130, du 20.09.1977 au 07.03.0978. La magicienne trahie : '
                 'Thorgal n’a qu’un tort : aimer Aaricia la fille de '
                 'Gandalf-le-fou roi des Vikings du Nord. C’est pour cela qu’il se '
                 'retrouve enchaîné à l’anneau des sacrifiés et voué à une mort '
                 'certaine. Thorgal doit son salut à Slive la reine de l’île des '
                 'Mers gelées qui a soif de vengeance envers Gandalf. En échange '
                 'de sa vie, Thorgal lui doit obéissance durant un an… Presque le '
                 'paradis… : Pour échapper à une meute de loup, Thorgal tombe dans '
                 'une crevasse profonde. Il se réveille dans un éden où vivent '
                 'trois sœurs et où le temps semble ne pas avoir d’empreintes sur '
                 'elles...',
        image="https://www.bedetheque.com/media/Couvertures/Couv_398.jpg"
    ),
    'BDFUGUE': Album(
        isbn=THORGAL_ISBN,
        title="la magicienne trahie",
        series="Thorgal",
        number="1",
        writer="Jean Van Hamme",
        illustrator="Grzegorz Rosinski",
        publisher="LOMBARD",
        publication_date=date(1996, 6, 7),
        number_of_pages=48,
        purchase_price=Decimal('6.00'),
        synopsis="Dès le début de l'histoire, Thorgal Aegirson est en mauvaise "
                 'posture : il est enchaîné à un rocher et est condamné à mourir, '
                 "noyé par la marée montante. Son crime est d'avoir osé aimer "
                 'Aaricia, la fille du roi des Vikings du Nord, lui, le bâtard né '
                 "d'on ne sait qui et on ne sait où. Il doit son salut à une "
                 'magicienne qui le sauve en échange de son obéissance...',
        image="https://www.bdfugue.com/media/catalog/product/cache/0d950bd4d3aaddc02a824ea154d9c41e/9/7/9782803603589_1_75.jpg"
    )
}

# LE VENT DANS LES SAULES

SAULE_ISBN = 9782840551072

# Données par source


SAULE_DATA = {
    'BDPHILE': Album(
        isbn=SAULE_ISBN,
        title="Le bois sauvage",
        series="Le Vent dans les saules",
        number="1",
        writer="Michel Plessix",
        illustrator="Michel Plessix",
        publisher="Delcourt",
        edition='6 rééditions',
        publication_date=date(1996, 10, 1),
        number_of_pages=30,
        purchase_price=Decimal('10.00'),
        synopsis="Qu'est ce qui lui prend à Taupe ? Les premiers rayons du soleil "
                 'lui auraient-ils tapé sur la tête ? Le voilà qui quitte, '
                 'guilleret, son trou empoussiéré pour musarder au bord de la '
                 "rivière. Il y rencontre Rat, s'en fait un ami embarque pour un "
                 'pique-nique improvisé, et vogue la galère !<br/>Le Vent dans les '
                 'Saules de Kenneth Grahame est un classique de la littérature '
                 'anglaise. Michel Plessix en tire une première interprétation en '
                 'bande dessinée qui ravira les lecteurs de 7 à 77 ans. Cette '
                 'histoire charmante met en scène une faune familière. Ce petit '
                 'monde vaque à ses occupations en costumes trois pièces et '
                 'cravates assorties et ne rechigne jamais à tremper un biscuit au '
                 'gingembre dans une tasse de thé. Les aventures épiques de Taupe '
                 "et consorts servent de prétexte à l'auteur pour brosser de "
                 "tendres tableaux bucoliques, travaillés jusqu'au moindre brin "
                 "d'herbe.<br/>Cela sent le foin, la vase. On respire. On se "
                 "détend. Notre barque file au gré du courant. Un filet d'eau "
                 'passe, vivace, entre nos orteils fripés et engourdis. La vie est '
                 'belle, le dépaysement garanti. Le Bois Sauvage est le premier '
                 'tome de la série.',
        image="https://static.bdphile.fr/images/media/cover/0007/7799.jpg"
    ),
    'BDGEST': Album(
        isbn=SAULE_ISBN,
        title="Le Bois Sauvage",
        series="Le vent dans les Saules",
        number="1",
        writer="Michel Plessix",
        illustrator="Michel Plessix",
        colorist="Michel Plessix",
        publisher="Delcourt",
        publication_date=date(1996, 10, 1),
        number_of_pages=31,
        purchase_price=Decimal('12.99'),
        synopsis="Qu'est ce qui lui prend à Taupe ? Les premiers rayons du soleil "
                 'lui auraient-ils tapé sur la tête ? Le voilà qui quitte, '
                 'guilleret, son trou empoussiéré pour musarder au bord de la '
                 "rivière. Il y rencontre Rat, s'en fait un ami embarque pour un "
                 'pique-nique improvisé, et vogue la galère ! Le Vent dans les '
                 'Saules de Kenneth Grahame est un classique de la littérature '
                 'anglaise. Michel Plessix en tire une première interprétation en '
                 'bande dessinée qui ravira les lecteurs de 7 à 77 ans. Cette '
                 'histoire charmante met en scène une faune familière. Ce petit '
                 'monde vaque à ses occupations en costumes trois pièces et '
                 'cravates assorties et ne rechigne jamais à tremper un biscuit au '
                 'gingembre dans une tasse de thé. Les aventures épiques de Taupe '
                 "et consorts servent de prétexte à l'auteur pour brosser de "
                 "tendres tableaux bucoliques, travaillés jusqu'au moindre brin "
                 "d'herbe. Cela sent le foin, la vase. On respire. On se détend. "
                 "Notre barque file au gré du courant. Un filet d'eau passe, "
                 'vivace, entre nos orteils fripés et engourdis. La vie est belle, '
                 'le dépaysement garanti.',
        image="https://www.bedetheque.com/media/Couvertures/Couv_931.jpg"
    ),
    'BDFUGUE': Album(
        isbn=SAULE_ISBN,
        title="le bois sauvage",
        series="Le vent dans les saules",
        number="1",
        writer="Michel Plessix",
        illustrator="Michel Plessix",
        colorist="Michel Plessix",
        publisher="DELCOURT",
        publication_date=date(2004, 1, 1),
        number_of_pages=0,
        synopsis="",
        purchase_price=Decimal('25.00'),
        image="https://www.bdfugue.com/media/catalog/product/cache/0d950bd4d3aaddc02a824ea154d9c41e/9/7/9782840551072_1_75.JPG"
    )
}
