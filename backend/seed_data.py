"""Realistic sample dataset for Meridian Library.

Book metadata (title/author/year/genre) is real public bibliographic
information used for demo purposes only; no copyrighted text is stored.
"""

ROOMS = [
    {
        "slug": "reading-nook",
        "name": "The Reading Nook",
        "category": "Quiet & Contemplative",
        "description": "A cozy corner room lined with curated shelves and window seats. Perfect for focused solo reading.",
        "level": 1,
        "capacity": 6,
        "status": "Open",
        "icon": "book",
    },
    {
        "slug": "archive-room",
        "name": "The Archive Room",
        "category": "Rare Collections",
        "description": "Climate-controlled archive housing rare manuscripts and first editions. Strict silence maintained.",
        "level": 3,
        "capacity": 2,
        "status": "Open",
        "icon": "scroll",
    },
    {
        "slug": "periodical-room",
        "name": "The Periodical Room",
        "category": "News & Journals",
        "description": "Current newspapers, journals and magazines in a bright, open reading hall.",
        "level": 2,
        "capacity": 12,
        "status": "Open",
        "icon": "newspaper",
    },
    {
        "slug": "map-room",
        "name": "The Map Room",
        "category": "Cartography & Geography",
        "description": "Large-format maps and atlases, with table space for spreading out historical charts.",
        "level": 2,
        "capacity": 8,
        "status": "Closed",
        "icon": "map",
    },
]

# how many of the 11 standard slots to pre-book for today, per room (for realism)
ROOM_PREBOOKED_COUNT = {
    "reading-nook": 6,
    "archive-room": 8,
    "periodical-room": 4,
    "map-room": 11,  # closed -> fully unavailable
}

TIME_SLOTS = [
    "09:00", "10:00", "11:00", "12:00", "13:00",
    "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
]

BOOKS = [
    # Computer Science
    {"call_no": "QA76.7 K47", "title": "The C Programming Language", "author": "Kernighan & Ritchie", "year": 1988, "genre": "Computer Science", "description": "The classic reference to the C language and its idioms.", "status": "Available"},
    {"call_no": "QA76.9 A25", "title": "Computer Networks", "author": "Tanenbaum, Andrew S.", "year": 2011, "genre": "Computer Science", "description": "A comprehensive tour of how computers and networks talk to each other.", "status": "Borrowed"},
    {"call_no": "QA76.6 H85", "title": "Introduction to Algorithms", "author": "Cormen, Thomas H. et al.", "year": 2009, "genre": "Computer Science", "description": "The standard graduate text on algorithm design and analysis.", "status": "Reserved"},
    {"call_no": "QA76.9 D32", "title": "Database System Concepts", "author": "Silberschatz et al.", "year": 2019, "genre": "Computer Science", "description": "Foundations of relational databases, transactions, and query processing.", "status": "Available"},
    {"call_no": "QA76.73 P98", "title": "Fluent Python", "author": "Ramalho, Luciano", "year": 2015, "genre": "Computer Science", "description": "Idiomatic, effective Python programming techniques.", "status": "Available"},
    {"call_no": "QA76.76 O63", "title": "Clean Code", "author": "Martin, Robert C.", "year": 2008, "genre": "Computer Science", "description": "Practices for writing readable, maintainable software.", "status": "Borrowed"},
    {"call_no": "QA76.9 A43", "title": "Designing Data-Intensive Applications", "author": "Kleppmann, Martin", "year": 2017, "genre": "Computer Science", "description": "How large-scale systems store, process, and move data reliably.", "status": "Available"},
    {"call_no": "QA76.758 S66", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "year": 1999, "genre": "Computer Science", "description": "Practical habits and tips for working software engineers.", "status": "Available"},
    # Mathematics
    {"call_no": "QA303 S84", "title": "Calculus", "author": "Stewart, James", "year": 2015, "genre": "Mathematics", "description": "A widely used undergraduate calculus textbook.", "status": "Available"},
    {"call_no": "QA39.3 R87", "title": "Linear Algebra Done Right", "author": "Axler, Sheldon", "year": 1997, "genre": "Mathematics", "description": "A conceptual, proof-first treatment of linear algebra.", "status": "Available"},
    {"call_no": "QA273 R69", "title": "A First Course in Probability", "author": "Ross, Sheldon", "year": 2019, "genre": "Mathematics", "description": "An introduction to probability theory with worked examples.", "status": "Reserved"},
    {"call_no": "QA248 H35", "title": "Naive Set Theory", "author": "Halmos, Paul", "year": 1960, "genre": "Mathematics", "description": "A short, classic introduction to set theory.", "status": "Available"},
    {"call_no": "QA9 H64", "title": "Godel, Escher, Bach", "author": "Hofstadter, Douglas", "year": 1979, "genre": "Mathematics", "description": "A sweeping exploration of logic, symmetry, and the mind.", "status": "Available"},
    # Self-Help
    {"call_no": "BF408 B56", "title": "How to Read a Book", "author": "Adler & Van Doren", "year": 1972, "genre": "Self-Help", "description": "A guide to active, purposeful reading at several levels.", "status": "Borrowed"},
    {"call_no": "BF637 S4 C37", "title": "How to Win Friends and Influence People", "author": "Carnegie, Dale", "year": 1936, "genre": "Self-Help", "description": "Timeless advice on communication and relationships.", "status": "Available"},
    {"call_no": "BJ1611 C68", "title": "The 7 Habits of Highly Effective People", "author": "Covey, Stephen R.", "year": 1989, "genre": "Self-Help", "description": "A framework for personal and professional effectiveness.", "status": "Available"},
    {"call_no": "BF637 S8 D83", "title": "Atomic Habits", "author": "Clear, James", "year": 2018, "genre": "Self-Help", "description": "How small, consistent habits compound into big change.", "status": "Reserved"},
    {"call_no": "BF408 C75", "title": "Deep Work", "author": "Newport, Cal", "year": 2016, "genre": "Self-Help", "description": "Rules for focused success in a distracted world.", "status": "Available"},
    # Essays
    {"call_no": "Z674.5 M67", "title": "The Library at Night", "author": "Manguel, Alberto", "year": 2006, "genre": "Essays", "description": "A meditation on libraries, reading, and the love of books.", "status": "Available"},
    {"call_no": "PS3566 I18 A6", "title": "Slouching Towards Bethlehem", "author": "Didion, Joan", "year": 1968, "genre": "Essays", "description": "Essays on California and American culture in the 1960s.", "status": "Available"},
    {"call_no": "PR6023 R8 A6", "title": "Consider the Lobster", "author": "Wallace, David Foster", "year": 2005, "genre": "Essays", "description": "A collection of reportage and cultural essays.", "status": "Borrowed"},
    {"call_no": "PN6071 E78", "title": "The Art of the Personal Essay", "author": "Lopate, Phillip (ed.)", "year": 1994, "genre": "Essays", "description": "An anthology spanning the history of the personal essay.", "status": "Available"},
    # Library Science
    {"call_no": "Z665 W55", "title": "The Pleasures of Libraries", "author": "Wilson, Leah", "year": 1995, "genre": "Library Science", "description": "An appreciation of libraries as places and institutions.", "status": "Available"},
    {"call_no": "Z678 L96", "title": "Library: An Unquiet History", "author": "Battles, Matthew", "year": 2003, "genre": "Library Science", "description": "A history of libraries from antiquity to today.", "status": "Available"},
    {"call_no": "Z716.4 G67", "title": "The Librarian's Book of Lists", "author": "Gordon, Rachel S.", "year": 2010, "genre": "Library Science", "description": "Practical checklists and references for library work.", "status": "Reserved"},
    # Fiction
    {"call_no": "PS3551 O764 N36", "title": "Never Let Me Go", "author": "Ishiguro, Kazuo", "year": 2005, "genre": "Fiction", "description": "A quietly devastating novel about memory and mortality.", "status": "Available"},
    {"call_no": "PQ2605 A3794 E813", "title": "The Stranger", "author": "Camus, Albert", "year": 1942, "genre": "Fiction", "description": "A classic of existentialist fiction.", "status": "Borrowed"},
    {"call_no": "PR9199.3 A8375 H35", "title": "The Handmaid's Tale", "author": "Atwood, Margaret", "year": 1985, "genre": "Fiction", "description": "A dystopian novel about control and resistance.", "status": "Available"},
    {"call_no": "PS3566 O87 M4", "title": "Beloved", "author": "Morrison, Toni", "year": 1987, "genre": "Fiction", "description": "A powerful novel about memory, trauma, and freedom.", "status": "Available"},
    # History
    {"call_no": "D743 K448", "title": "The Second World War", "author": "Keegan, John", "year": 1989, "genre": "History", "description": "A one-volume military history of the Second World War.", "status": "Available"},
    {"call_no": "DS119.7 M67", "title": "The Lemon Tree", "author": "Tolan, Sandy", "year": 2006, "genre": "History", "description": "A true story of the Israeli-Palestinian conflict told through two families.", "status": "Reserved"},
    {"call_no": "E183.7 Z55", "title": "A People's History of the United States", "author": "Zinn, Howard", "year": 1980, "genre": "History", "description": "American history told from the perspective of ordinary people.", "status": "Available"},
    # Science
    {"call_no": "QC173.59 S65 S65", "title": "A Brief History of Time", "author": "Hawking, Stephen", "year": 1988, "genre": "Science", "description": "An accessible introduction to cosmology and the nature of time.", "status": "Available"},
    {"call_no": "QH366.2 D39", "title": "The Selfish Gene", "author": "Dawkins, Richard", "year": 1976, "genre": "Science", "description": "A gene-centered view of evolution and natural selection.", "status": "Borrowed"},
    {"call_no": "QP376 S23", "title": "The Brain That Changes Itself", "author": "Doidge, Norman", "year": 2007, "genre": "Science", "description": "Stories of neuroplasticity and the adaptable human brain.", "status": "Available"},
    {"call_no": "QC16 F49 B49", "title": "Surely You're Joking, Mr. Feynman", "author": "Feynman, Richard", "year": 1985, "genre": "Science", "description": "Anecdotes from the life of physicist Richard Feynman.", "status": "Available"},
    # Philosophy
    {"call_no": "B3376 W564 T7", "title": "Tractatus Logico-Philosophicus", "author": "Wittgenstein, Ludwig", "year": 1921, "genre": "Philosophy", "description": "A foundational, aphoristic text of 20th-century philosophy.", "status": "Available"},
    {"call_no": "B2430 C34 E5", "title": "The Myth of Sisyphus", "author": "Camus, Albert", "year": 1942, "genre": "Philosophy", "description": "An essay on the absurd and the meaning of life.", "status": "Reserved"},
    {"call_no": "BJ1012 S26", "title": "The Righteous Mind", "author": "Haidt, Jonathan", "year": 2012, "genre": "Philosophy", "description": "Why good people are divided by politics and religion.", "status": "Available"},
    # Art
    {"call_no": "N7445.2 B47", "title": "Ways of Seeing", "author": "Berger, John", "year": 1972, "genre": "Art", "description": "A foundational text on how we look at and interpret images.", "status": "Available"},
    {"call_no": "ND237 O39", "title": "Georgia O'Keeffe: A Life", "author": "Robinson, Roxana", "year": 1989, "genre": "Art", "description": "A biography of the American modernist painter.", "status": "Available"},
    # Biography
    {"call_no": "CT275 F8273 A3", "title": "The Diary of a Young Girl", "author": "Frank, Anne", "year": 1947, "genre": "Biography", "description": "The wartime diary of a young girl in hiding.", "status": "Borrowed"},
    {"call_no": "E457 C215", "title": "Team of Rivals", "author": "Goodwin, Doris Kearns", "year": 2005, "genre": "Biography", "description": "A political biography of Abraham Lincoln and his cabinet.", "status": "Available"},
    {"call_no": "E449 D75", "title": "Narrative of the Life of Frederick Douglass", "author": "Douglass, Frederick", "year": 1845, "genre": "Biography", "description": "Douglass's own account of his life in slavery and his path to freedom.", "status": "Available"},
    {"call_no": "E444 N67", "title": "Twelve Years a Slave", "author": "Northup, Solomon", "year": 1853, "genre": "Biography", "description": "A memoir of a free man kidnapped and sold into slavery.", "status": "Reserved"},

    # Classic Fiction (sourced from Open Library's public catalogue; publication
    # years cross-checked and corrected against standard bibliographic references)
    {"call_no": "PR4034 P7", "title": "Pride and Prejudice", "author": "Austen, Jane", "year": 1813, "genre": "Fiction", "description": "A witty novel of manners, marriage, and misjudgment in Regency England.", "status": "Available"},
    {"call_no": "PR4611 A73", "title": "Alice's Adventures in Wonderland", "author": "Carroll, Lewis", "year": 1865, "genre": "Fiction", "description": "A young girl's surreal journey down a rabbit hole.", "status": "Available"},
    {"call_no": "PR4572 C68", "title": "A Christmas Carol", "author": "Dickens, Charles", "year": 1843, "genre": "Fiction", "description": "A miser is visited by three spirits on Christmas Eve.", "status": "Borrowed"},
    {"call_no": "PR5819 P5", "title": "The Picture of Dorian Gray", "author": "Wilde, Oscar", "year": 1890, "genre": "Fiction", "description": "A man stays young while his portrait bears the marks of his sins.", "status": "Available"},
    {"call_no": "PR4172 W7", "title": "Wuthering Heights", "author": "Bronte, Emily", "year": 1847, "genre": "Fiction", "description": "A dark, stormy tale of love and revenge on the Yorkshire moors.", "status": "Available"},
    {"call_no": "PS1305 A1", "title": "Adventures of Huckleberry Finn", "author": "Twain, Mark", "year": 1884, "genre": "Fiction", "description": "A boy and an escaped enslaved man raft down the Mississippi.", "status": "Available"},
    {"call_no": "PS1868 S3", "title": "The Scarlet Letter", "author": "Hawthorne, Nathaniel", "year": 1850, "genre": "Fiction", "description": "A woman is publicly shamed in Puritan New England.", "status": "Reserved"},
    {"call_no": "PR3403 R6", "title": "Robinson Crusoe", "author": "Defoe, Daniel", "year": 1719, "genre": "Fiction", "description": "A shipwrecked man survives alone on a remote island for decades.", "status": "Available"},
    {"call_no": "PR4034 E5", "title": "Emma", "author": "Austen, Jane", "year": 1815, "genre": "Fiction", "description": "A well-meaning matchmaker learns to understand her own heart.", "status": "Available"},
    {"call_no": "PR4568 O4", "title": "Oliver Twist", "author": "Dickens, Charles", "year": 1838, "genre": "Fiction", "description": "An orphan navigates poverty and crime in Victorian London.", "status": "Available"},
    {"call_no": "PR5397 F7", "title": "Frankenstein", "author": "Shelley, Mary", "year": 1818, "genre": "Fiction", "description": "A scientist's creation turns against him.", "status": "Borrowed"},
    {"call_no": "PR4034 S4", "title": "Sense and Sensibility", "author": "Austen, Jane", "year": 1811, "genre": "Fiction", "description": "Two sisters navigate love and financial hardship.", "status": "Available"},
    {"call_no": "PR4571 T2", "title": "A Tale of Two Cities", "author": "Dickens, Charles", "year": 1859, "genre": "Fiction", "description": "A story of sacrifice set against the French Revolution.", "status": "Available"},
    {"call_no": "PZ7 B3267", "title": "The Wonderful Wizard of Oz", "author": "Baum, L. Frank", "year": 1900, "genre": "Fiction", "description": "A girl is swept to a magical land and seeks a way home.", "status": "Available"},
    {"call_no": "PR5489 T7", "title": "Treasure Island", "author": "Stevenson, Robert Louis", "year": 1883, "genre": "Fiction", "description": "A young boy sets sail on a hunt for buried pirate gold.", "status": "Available"},
    {"call_no": "PR6037 T617 D7", "title": "Dracula", "author": "Stoker, Bram", "year": 1897, "genre": "Fiction", "description": "A gothic tale of a Transylvanian vampire's arrival in England.", "status": "Reserved"},
    {"call_no": "PS1016 L5", "title": "Little Women", "author": "Alcott, Louisa May", "year": 1868, "genre": "Fiction", "description": "Four sisters come of age during and after the Civil War.", "status": "Available"},
    {"call_no": "PS3523 O46 C3", "title": "The Call of the Wild", "author": "London, Jack", "year": 1903, "genre": "Fiction", "description": "A domesticated dog reverts to his wild instincts in the Yukon.", "status": "Available"},
    {"call_no": "PR3724 G7", "title": "Gulliver's Travels", "author": "Swift, Jonathan", "year": 1726, "genre": "Fiction", "description": "A satirical voyage to lands of tiny and giant people.", "status": "Available"},
    {"call_no": "PQ6329 A1", "title": "Don Quixote", "author": "Cervantes, Miguel de", "year": 1605, "genre": "Fiction", "description": "A would-be knight sets out on delusional chivalric adventures.", "status": "Available"},
    {"call_no": "PG3366 A6", "title": "Anna Karenina", "author": "Tolstoy, Leo", "year": 1877, "genre": "Fiction", "description": "A tragic love affair set against Russian high society.", "status": "Borrowed"},
    {"call_no": "PR6023 O48 D8", "title": "Dubliners", "author": "Joyce, James", "year": 1914, "genre": "Fiction", "description": "A collection of short stories portraying everyday life in Dublin.", "status": "Available"},
    {"call_no": "PG3328 Z7 N6", "title": "Notes from Underground", "author": "Dostoevsky, Fyodor", "year": 1864, "genre": "Fiction", "description": "A bitter, isolated narrator rails against society and reason.", "status": "Available"},

    # Poetry
    {"call_no": "PS3222 L4", "title": "Leaves of Grass", "author": "Whitman, Walt", "year": 1855, "genre": "Poetry", "description": "A sweeping, free-verse celebration of democracy and the self.", "status": "Available"},
    {"call_no": "PR1850 A1", "title": "The Canterbury Tales", "author": "Chaucer, Geoffrey", "year": 1400, "genre": "Poetry", "description": "A frame narrative of pilgrims' tales on the road to Canterbury.", "status": "Available"},
    {"call_no": "PQ4315 A1", "title": "The Divine Comedy", "author": "Dante Alighieri", "year": 1320, "genre": "Poetry", "description": "A visionary journey through Hell, Purgatory, and Paradise.", "status": "Reserved"},

    # Drama
    {"call_no": "PR2807 A1", "title": "Hamlet", "author": "Shakespeare, William", "year": 1603, "genre": "Drama", "description": "A Danish prince is haunted by his father's murder and his own indecision.", "status": "Available"},
    {"call_no": "PR2823 A1", "title": "Macbeth", "author": "Shakespeare, William", "year": 1623, "genre": "Drama", "description": "Ambition and prophecy drive a Scottish general to murder.", "status": "Available"},
    {"call_no": "PR2829 A1", "title": "Othello", "author": "Shakespeare, William", "year": 1622, "genre": "Drama", "description": "Jealousy, manipulated by Iago, destroys a general's marriage.", "status": "Borrowed"},
    {"call_no": "PR2808 A1", "title": "Julius Caesar", "author": "Shakespeare, William", "year": 1599, "genre": "Drama", "description": "Roman senators conspire against Caesar, with bloody consequences.", "status": "Available"},

    # More Philosophy
    {"call_no": "JC143 M4", "title": "The Prince", "author": "Machiavelli, Niccolo", "year": 1532, "genre": "Philosophy", "description": "A pragmatic, unsentimental guide to acquiring and keeping political power.", "status": "Available"},
]

EVENTS = [
    {
        "title": "Intro to Research Databases Workshop",
        "description": "Hands-on session covering how to search academic databases and citation tools.",
        "date": "2026-10-15",
        "time": "10:00",
        "type": "Workshop",
        "capacity": 20,
        "registered_count": 11,
    },
    {
        "title": "Monthly Reading Circle: Contemporary Fiction",
        "description": "This month's pick is discussed over coffee in the Reading Nook.",
        "date": "2026-10-18",
        "time": "17:30",
        "type": "Reading Circle",
        "capacity": 15,
        "registered_count": 9,
    },
    {
        "title": "Local History Seminar: Founding of Meridian",
        "description": "A talk on the town's founding, drawing from the Archive Room's collection.",
        "date": "2026-10-22",
        "time": "15:00",
        "type": "Seminar",
        "capacity": 30,
        "registered_count": 14,
    },
    {
        "title": "Poetry Open Mic Night",
        "description": "Share your own poetry or just come to listen, in the Periodical Room.",
        "date": "2026-10-25",
        "time": "18:00",
        "type": "Community",
        "capacity": 40,
        "registered_count": 22,
    },
    {
        "title": "Resume & Career Resources Drop-in",
        "description": "Librarians on hand to help with resumes, job search tools, and databases.",
        "date": "2026-10-29",
        "time": "14:00",
        "type": "Workshop",
        "capacity": 10,
        "registered_count": 4,
    },
]

LIBRARY_STATS = {
    "total_books": 84621,
    "reading_rooms": 4,
    "members": 1204,
}

DEMO_MEMBER = {
    "name": "Gaurav Kumar",
    "email": "gaurav@gmail.com",
    "password": "demo1234",
    "member_since": "2024-03-11",
}
