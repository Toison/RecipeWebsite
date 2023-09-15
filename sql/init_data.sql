PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('bg', 'Beluga', 'bg@kmail.ru','bg.jpeg','sha512$b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('sc', 'Skittle Chan', 'xxx@kmail.ru','sc.png','sha512$b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('Gao516', 'Runshi Gao', 'rsgao@umich.edu','dog.webp','123456');


INSERT INTO posts(postid, owner, recipename)
VALUES (1, 'bg', 'Smothered Chicken Thighs in Onion Gravy');

INSERT INTO posts(postid, owner, recipename)
VALUES (2, 'Gao516', 'Teriyaki Chicken');

INSERT INTO posts(postid, owner, recipename)
VALUES (3, 'Gao516', 'Garlic Rib');

INSERT INTO posts(postid, owner, recipename)
VALUES (4, 'Gao516', 'Thai Hot Shrimp');

INSERT INTO posts(postid, owner, recipename)
VALUES (5, 'Gao516', 'Oreo Ice Cream');

INSERT INTO posts(postid, owner, recipename)
VALUES (6, 'Gao516', 'Red Brew Chicken Wings');

INSERT INTO following(follower, followee)
VALUES ('sc', 'bg');

INSERT INTO comments(commentid, commenter, postid, text, ratevalue)
VALUES (1, 'sc', 1, 'Very delicious!', 4);

INSERT INTO comments(commentid, commenter, postid, text, ratevalue)
VALUES (2, 'sc', 1, 'Very well explained, nice job!', 4);

INSERT INTO comments(commentid, commenter, postid, text, ratevalue)
VALUES (3, 'sc', 1, 'It really works! Try it out guys!', 5);

INSERT INTO likes(liker, postid)
VALUES ('sc', 1);

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (1, 1, 'step1.webp', 'Pat the chicken thighs dry using a paper towel. Place chicken in the flour-spice mixture to coat on both sides. Shake off the excess flour (and make sure to set the flour aside, you’ll need it to make the gravy).');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (1, 2, 'step2.webp', 'Add the coated thighs to the pan without crowding and sear in two batches (if necessary) until golden brown, 1 to 2 minutes per side. Set chicken aside on a plate.');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (1, 3, 'step3.webp', 'Add to the skillet the reserved chicken thighs with any accumulated juices, thyme sprigs, and the bay leaf. Nestle the thighs into the onions and turn to coat all sides in the gravy.');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (1, 4, 'step4.webp', 'Transfer the skillet to the oven, uncovered, and cook until the juices of the chicken run clear when pierced with a knife and the temperature reads 165°F when inserted with an instant-read thermometer, 20 to 25 minutes.If the gravy seems too thick, remove the chicken thighs to a serving plate and add chicken stock a little at a time. (The sauce should be thick enough to coat a spoon.)');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 1, '1.jpeg', 'Separate the flesh and bones, break the tendons, use a sharp knife to pay attention to safety!');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 2, '2.jpeg', 'The flesh and bones are well separated, just poke the tip of the knife, don’t waste the bones, you can cook soup');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 3, '3.jpeg', 'Sprinkle some salt, pepper, soy sauce, put it in the refrigerator to marinate for an hour');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 4, '4.jpeg', 'Without oil, fry the chicken skin side first, fry until golden brown and fry the other side until golden brown');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 5, '5.jpeg', 'Mix ginger and garlic, mirin, oil consumption, soy sauce, dark soy sauce, honey, water, etc., stir together and pour into the pot. (As for how much juice you put in, it depends on how long you think the chicken legs will be cooked.) Cover the pot and cook for 20 minutes or so! Don not use too much heat, turn it over in 5 minutes!');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (2, 6, '6.jpeg', 'Collect the sauce over high heat, cut the chicken thighs on a plate, and drizzle with the sauce');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (3, 1, '31.jpeg', 'First marinate the ribs');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (3, 2, '32.jpeg', 'Rinse the ribs, add minced garlic, half a spoon of salt, a spoon of sugar, two spoons of soy sauce, a spoon of cooking wine, a spoon of oyster sauce, and two spoons of starch, mix well and marinate for two hours to taste');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (3, 3, '33.jpeg', 'Heat a proper amount of oil in the pot until the chopsticks touch it and it will bubbling. Put the pork ribs in pieces, and fry slowly on low heat until both sides are golden brown, fry for about 10 minutes, remove them');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (3, 4, '34.jpeg', 'Heat the oil in a pot over medium heat, pour in the ribs and fry for a minute.');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (4, 1, '41.jpeg', '1: Remove the head of the prawn and remove the shrimp line
2: Put 2 slices of ginger in boiling water and blanch
3: Rinse in cold water to peel off easily, pull out the shrimp for later use');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (4, 2, '42.jpeg', '1: Preparation: 2 slices of lemon, 2 parsleys, cut into sections, 4 pieces of spicy millet, half of an onion, diced, 1 passion fruit, 8 cloves of garlic');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (4, 3, '43.jpeg', '1: Put shrimp in a bowl and pour in all the ingredients
2: Seasoning juice: 2 spoons of soy sauce, 1 spoon of oyster sauce, 1 spoon of vinegar, 1 spoon of lemon juice, 1 spoon of sugar, 1 spoon of white sesame oil, 1 spoon of sesame oil');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (4, 4, '44.jpeg', 'Finally, grab and mix evenly, and you can start eating; the taste is really super good!');


INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (5, 1, '51.jpeg', 'Whipped cream + caster sugar');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (5, 2, '52.jpeg', 'Add yogurt and crushed Oreos and mix well');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (5, 3, '53.jpeg', 'Freeze in paper cups');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (5, 4, '54.jpeg', 'Cover with a layer of Oreos on each side. Done!');


INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (6, 1, '61.jpeg', 'Shred and slice ginger, green onion, and minced garlic for use. The shredded ginger and garlic on the left is used for marinating chicken wings, and the one on the right is used for stir-frying.');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (6, 2, '62.jpeg', 'Pour 3 spoons of cooking wine, 2 spoons of soy sauce, 1/2 spoon of cornstarch, ginger and garlic into the chicken wings and marinate for 15-20 minutes');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (6, 3, '63.jpeg', 'Heat oil in a pan, add onion, ginger and garlic and saute until fragrant');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (6, 4, '64.jpeg', 'Put the chicken wings into the pot and stir-fry for a few times, add hot water that has not covered the chicken wings, and then bring to a boil, add onion knots, rock sugar, oyster sauce, 1/2 tablespoon of dark soy sauce, 1/2 tablespoon of light soy sauce, turn to low heat and simmer for 15 minutes, then take out the onion and ginger slices, and collect the juice over high heat.');

INSERT INTO steps(postid, stepnum, imgpath, text)
VALUES (6, 5, '65.jpeg', 'Sprinkle sesame and chopped green onion out of the pot, let us eat! Really delicious cannot stop');

INSERT INTO tags(postid, tagid)
VALUES (1, 7);

INSERT INTO tags(postid, tagid)
VALUES (1, 5);

INSERT INTO tags(postid, tagid)
VALUES (2, 2);

INSERT INTO tags(postid, tagid)
VALUES (2, 7);

INSERT INTO tags(postid, tagid)
VALUES (2, 13);

INSERT INTO tags(postid, tagid)
VALUES (3, 1);

INSERT INTO tags(postid, tagid)
VALUES (3, 12);

INSERT INTO tags(postid, tagid)
VALUES (3, 15);

INSERT INTO tags(postid, tagid)
VALUES (4, 4);

INSERT INTO tags(postid, tagid)
VALUES (4, 10);

INSERT INTO tags(postid, tagid)
VALUES (4, 14);

INSERT INTO tags(postid, tagid)
VALUES (4, 16);

INSERT INTO tags(postid, tagid)
VALUES (5, 8);

INSERT INTO tags(postid, tagid)
VALUES (5, 11);

INSERT INTO tags(postid, tagid)
VALUES (5, 13);

INSERT INTO tags(postid, tagid)
VALUES (6, 1);

INSERT INTO tags(postid, tagid)
VALUES (6, 13);

INSERT INTO tags(postid, tagid)
VALUES (6, 7);

INSERT INTO tags(postid, tagid)
VALUES (6, 15);
