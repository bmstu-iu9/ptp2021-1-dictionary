let parse_tests = [
    {
        test: "опыт",
        right: ["опыт"]
    },
    {
        test: "прорыв, достижение",
        right: ["прорыв", "достижение"]
    },
    {
        test: "принимать, брать на себя, считать, полагать",
        right: ["принимать", "брать на себя", "считать", "полагать"]
    },
    {
        test: "клавиша/ключ доступа",
        right: ["клавиша", "ключ доступа"]
    },
    {
        test: "(по)следствие, результат ",
        right: ["последствие", "следствие", "результат"]
    },
    {
        test: "изменять(ся), менять(ся)",
        right: ["изменять", "изменяться", "менять", "меняться"]
    },
    {
        test: "breakthrough ",
        right: ["breakthrough"]
    },
    {
        test: "thin layer of insulator ",
        right: ["thin layer of insulator"]
    }
];

describe("parse", function () {
    for (let i = 0; i < parse_tests.length; i++) {
        let w = parse(parse_tests[i].test);
        let k = 0;
        for (let j = 0; j < parse_tests[i].right.length; j++) {
            if (w.includes(parse_tests[i].right[j])) {
                k++;
            }
        }
        let s = w.join("\" \"");
        it("\"" + parse_tests[i].test + "\" разделяется на \"" + s + "\"", function () {
            assert.isTrue((w.length == parse_tests[i].right.length) && (k == parse_tests[i].right.length));
        });
    }
});