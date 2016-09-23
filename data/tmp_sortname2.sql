-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 23, 2016 at 12:09 AM
-- Server version: 5.5.50-cll
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `bco2676_rtsunlimited`
--
-- --------------------------------------------------------

--
-- Table structure for table `tmp_sortname`
--





USE rts_db;

CREATE TABLE IF NOT EXISTS `tmp_sortname` (
  `id` int(11) NOT NULL,
  `sort_name` varchar(255) NOT NULL,
  UNIQUE KEY `idx_name` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tmp_sortname`
--

INSERT INTO `tmp_sortname` (`id`, `sort_name`) VALUES
(4866, 'nineteensixtythree'),
(1937, 'Amazing Adventures'),
(1570, 'Amazing Spider-Man'),
(1635, 'Amazing Spider-Man Annual'),
(1489, 'Atom'),
(141, 'Batman'),
(1468, 'Batman Annual'),
(1098, 'Brave and the Bold'),
(1860, 'Captain America'),
(2044, 'Cat'),
(4634, 'Catwoman Signed'),
(2424, 'Cerebus'),
(3301, 'Dark Horse Presents'),
(4238, 'Deathlok'),
(1863, 'Doctor Strange'),
(3179, 'Droids'),
(1482, 'Fantastic Four'),
(2912, 'Flaming Carrot Comics'),
(1448, 'Green Lantern'),
(4492, 'Harbinger'),
(1623, 'Hawkman'),
(1866, 'Incredible Hulk'),
(16141, 'Invaders'),
(1867, 'Iron Man'),
(538, 'Lone Ranger'),
(3845, 'Marc Spector: Moon Knight'),
(2055, 'Marvel Premiere'),
(1745, 'Marvel Super Heroes'),
(1554, 'Metal Men'),
(159, 'National Comics'),
(4035, 'New Warriors'),
(4852, 'Prime'),
(3720, 'Rocketeer Adventure Magazine'),
(1194, 'Showcase'),
(4611, 'Spawn'),
(824, 'Strange Tales'),
(1874, 'Sub-Mariner'),
(1732, 'Swing With Scooter'),
(1442, 'Tales of Suspense'),
(1443, 'Tales To Astonish'),
(1749, 'Thor'),
(50383, 'Thundercats'),
(12530, 'Vampirellav'),
(3497, 'Walt Disney''s Uncle Scrooge Adventures'),
(3209, 'X-Factor'),
(1576, 'X-Men'),
(1951, 'X-Men1Annual'),
(2359, 'Spectacular Spider-Man'),
(97, 'Action Comics'),
(14172, 'Addams Family'),
(98, 'Adventure Comics'),
(598, 'Adventures into the Unknown'),
(862, 'Adventures of Dean Martin & Jerry Lewis'),
(372, 'Air Ace'),
(10512, 'Amazing World of DC Comics'),
(11548, 'ApprovedComics'),
(1571, 'Avengers'),
(344, 'Blackhawk'),
(202, 'Blue Bolt'),
(34466, 'Blue Bolt'),
(756, 'Bobby Benson''s B-Bar-B Riders'),
(295, 'Boy Comics'),
(248, 'Bulletman'),
(1861, 'Captain Marvel'),
(307, 'Captain Midnight'),
(2094, 'Champion Sports'),
(10765, 'Classic Comics'),
(11711, 'Comic Comics'),
(1939, 'Conan The Barbarian'),
(296, 'Crime Does Not Pay'),
(759, 'Crime Suspenstories'),
(11279, 'Cycletoons'),
(1636, 'Daredevil'),
(235, 'Daredevil Comics'),
(177, 'Daring Mystery Comics'),
(87, 'Detective Comics'),
(11621, 'Dick Tracy'),
(224, 'Doll Man'),
(872, 'Donald Duck'),
(1622, 'Doom Patrol'),
(2086, 'E-Man'),
(1151, 'Extra!'),
(1425, 'Famous Monsters of Filmland'),
(18291, 'Fantagor'),
(712, 'Feature Presentation'),
(3096, 'Femforce'),
(1428, 'Flash'),
(2026, 'Forbidden Tales of Dark Mansion'),
(837, 'Forbidden Worlds'),
(279, 'Four Color'),
(243, 'Four Favorites'),
(834, 'Frontline Combat'),
(1817, 'Girl From U.N.C.L.E.'),
(791, 'House of Mystery'),
(1192, 'House of Secrets'),
(2347, 'Howard the Duck'),
(1762, 'ISpy'),
(12582, 'Indians'),
(11772, 'Jetsons'),
(19295, 'Johnny Hazard'),
(773, 'Jon Juan'),
(896, 'Journey Into Mystery'),
(19296, 'Jungle Jim'),
(1449, 'Justice League of America'),
(82, 'King Comics'),
(1447, 'Konga'),
(2099, 'Legion of Super-Heroes'),
(10092, 'Mad'),
(7695, 'Man From U.N.C.L.E.'),
(1992, 'Marvel Spotlight'),
(2180, 'Marvel Treasury Edition'),
(1671, 'Metamorpho'),
(1980, 'Mister Miracle'),
(402, 'Modern Comics'),
(74, 'More Fun Comics'),
(17116, 'Motor City Comics'),
(11399, 'My Little Margie'),
(1981, 'New Gods'),
(11651, 'New Romances'),
(2151, 'Omac'),
(2356, 'Omega the Unknown'),
(868, 'Our Army At War'),
(1630, 'Outer Limits'),
(1064, 'Piracy'),
(162, 'Planet Comics'),
(615, 'Pogo Possum'),
(226, 'Police Comics'),
(84, 'Popular Comics'),
(1485, 'Reptisaurus'),
(1470, 'Sea Devils'),
(913, 'Shock Suspenstories'),
(1872, 'Silver Surfer'),
(17089, 'Slow Death Funnies'),
(2268, 'Son of Satan'),
(936, 'SpaceAdventures'),
(944, 'Star Spangled War Stories'),
(2406, 'Star Wars'),
(2519, 'Star Wars Annual'),
(758, 'Straight Arrow'),
(704, 'Strange Adventures'),
(13806, 'Strange Suspense Stories'),
(116, 'Superman'),
(1451, 'Superman1Annual'),
(2062, 'SupernaturalThrillers'),
(1196, 'Tales of the Unexpected'),
(543, 'Tarzan'),
(859, 'Terrors of the Jungle'),
(12452, 'Thrilling Crime Cases'),
(12735, 'Tom Mix Western'),
(1915, 'Tower of Shadows'),
(73711, 'Two Fisted Tales'),
(966, 'Uncle Scrooge'),
(1774, 'Undersea Agent'),
(1857, 'Unexpected'),
(1460, 'Unknown Worlds'),
(1916, 'Vampirella'),
(153, 'Walt Disney''s Comics and Stories'),
(528, 'Wanted Comics'),
(216, 'World''s Finest Comics'),
(387, 'Yellowjacket Comics'),
(1892, 'Zap Comix'),
(11606, 'Beverly Hillbillies'),
(11364, 'Brenda Starr'),
(12492, 'Crime Detective Comics'),
(14223, 'Exotic Romances'),
(7765, 'Famous First Edition'),
(11627, 'Felix the Cat'),
(11632, 'Flipper'),
(769, 'Geronimo'),
(1735, 'Get Smart'),
(172, 'Green Mask'),
(11455, 'Hot Rod Racers'),
(694, 'Hot Rods and Racing Cars'),
(513, 'Justice Traps The Guilty'),
(9960, 'Meridian'),
(792, 'Mystery in space'),
(9959, 'Mystic'),
(1025, 'Our Fighting Forces'),
(900, 'Patsy and Hedy'),
(1533, 'Phantom'),
(741, 'Romantic Affairs'),
(13409, 'Roy Rogers'' Trigger'),
(12413, 'Sad Sack Comics'),
(13060, 'Saint'),
(9961, 'Scion'),
(9962, 'Sigil'),
(11915, 'Sweethearts'),
(10273, 'Tales Too Terrible To Tell'),
(1427, 'TeenConfessions'),
(11465, 'TeenageHotrodders'),
(11381, 'Valley of the Dinosaurs'),
(1656, 'Voyage to the Bottom of the Sea'),
(189, 'Whiz Comics'),
(163, 'Wings Comics'),
(967, 'Adventures in 3-D'),
(464, 'All Great Comics'),
(1488, 'Aquaman'),
(1847, 'Atom & Hawkman'),
(14630, 'Barnyard Comics'),
(1849, 'Beware the Creeper'),
(624, 'Black Diamond Western'),
(16057, 'Boy Meets Girl'),
(27359, 'Bringing Up Father'),
(27360, 'Bringing Up Father The Big Book'),
(13993, 'Buck Rogers'),
(17305, 'Captain Atom'),
(13189, 'Captain Easy'),
(249, 'Captain Marvel Adventures'),
(306, 'Captain Marvel Jr.'),
(1293, 'Challengers of the Unknown'),
(16555, 'Charlie McCarthy'),
(552, 'Crime and Punishment'),
(13589, 'Darling Love'),
(495, 'Date with Judy'),
(331, 'Don Winslow of the Navy'),
(18806, 'Eighty-Seventh Precinct'),
(713, 'Feature Presentations'),
(918, 'Fighting Undersea Commandos'),
(1977, 'Forever People'),
(12606, 'Frisky Fables'),
(342, 'Funny Stuff'),
(848, 'gijoe'),
(12556, 'Gangsters Can''t Win'),
(18396, 'Gene Autry Comics'),
(1979, 'Ghosts'),
(608, 'Girls Love Stories'),
(13199, 'Goofy Comics'),
(11763, 'Great Lover Romances'),
(13542, 'Hand of Fate'),
(12169, 'Heart Throbs'),
(26691, 'Henry Hardback'),
(10951, 'Hopalong Cassidy'),
(1794, 'Inferior Five'),
(161, 'Jungle Comics'),
(1041, 'Jungle Tales'),
(1617, 'Jungle Tales of Tarzan'),
(213, 'Leading Comics'),
(534, 'Leave it to Binky'),
(15533, 'LittleAbner'),
(27361, 'Little Orphan Annie'),
(7069, 'Looney Tunes and Merrie Melodies Comics'),
(648, 'Love Romances'),
(13591, 'Lovelorn'),
(1450, 'Many Loves of Dobie Gillis'),
(482, 'March of Comics'),
(655, 'Marvel Tales'),
(854, 'Mister Universe'),
(12612, 'Monte Hale Western'),
(114, 'Mutt & Jeff'),
(1103, 'My Greatest Adventure'),
(1811, 'Not Brand Echh'),
(425, 'Nyoka The Jungle Girl'),
(31395, 'Oh Skin-nay!'),
(419, 'Patsy Walker'),
(690, 'Perfect Crime'),
(15404, 'Perfect Love'),
(18202, 'Personal Love'),
(1903, 'Phantom Stranger'),
(11918, 'Picture Stories from Science'),
(318, 'Plastic Man'),
(2102, 'Plop!'),
(1185, 'Public Defender in Action'),
(935, 'Racket Squad in Action'),
(12490, 'Real Life Comics'),
(1247, 'Robin Hood Tales'),
(13072, 'Rocky Lane Western'),
(13462, 'Romantic Marriage'),
(2153, 'Sandman'),
(15027, 'Secret Romances'),
(1855, 'Secret Six'),
(1248, 'Sergeant Bilko'),
(2105, 'Shadow'),
(51808, 'Smitty'),
(838, 'Soldiers of Fortune'),
(223, 'Sparkler Comics'),
(1795, 'Spectre'),
(107, 'SuperComics'),
(614, 'Superboy'),
(203, 'Target Comics'),
(19256, 'Target: the Corruptors'),
(20153, 'Tex Farrell'),
(1197, 'Three Mouseketeers'),
(271, 'True Comics'),
(12525, 'True Sport Picture Stories'),
(13853, 'Underworld'),
(12460, 'Worlds of Fear'),
(15039, 'Young Brides'),
(695, 'Adventures of Bob Hope'),
(1478, 'Adventures of the Jaguar'),
(426, 'Airboy Comics'),
(11612, 'Billy The Kid Adventure Magazine'),
(14005, 'Blazing Western'),
(12824, 'Bruce Gentry'),
(1022, 'Dodo and the Frog'),
(2658, 'Marvel Graphic Novel'),
(14123, 'Exploits of Daniel Boone'),
(17702, 'Faust'),
(122, 'Feature Comics'),
(544, 'Firehair Comics'),
(12602, 'Flintstones'),
(11419, 'Flintstones'),
(865, 'Flippity & Flop'),
(11633, 'Flyboy'),
(11746, 'Funny Films'),
(8111, 'Funny Folks'),
(11749, 'Gabby Hayes Western'),
(19884, 'Living Bible'),
(1078, 'Masked Ranger'),
(26170, 'Men in Black'),
(1680, 'Mighty Crusaders'),
(60438, 'Movie Classics'),
(43476, 'Moving Fortress'),
(1289, 'Outer Space'),
(1429, 'Pat Boone'),
(16550, 'Pay-Off'),
(11917, 'Picture Stories from World History'),
(1132, 'Rawhide Kid'),
(400, 'Real Screen Comics'),
(20278, 'Real West Romances'),
(12837, 'Robin Hood Tales'),
(1995, 'Savage Tales'),
(1094, 'Scotland Yard'),
(19362, 'Special Agent'),
(12732, 'Swords Of Cerebus'),
(3115, 'Tales of the Beanworld'),
(13694, 'Texan'),
(12440, 'Three Stooges'),
(705, 'Tomahawk'),
(11731, 'Top Secrets'),
(1158, 'Valor'),
(537, 'Western Comics'),
(10082, 'Worst From Mad'),
(14361, 'Young Eagle'),
(44157, 'Zen Intergalactic Ninja'),
(1845, 'Angel and the Ape'),
(1846, 'Anthro'),
(12645, 'Archie''s Pal Jughead'),
(790, 'Big Town'),
(559, 'Blaze Carson'),
(1499, 'Fury'),
(879, 'GICombat'),
(496, 'Gang Busters'),
(1878, 'Garrison''s Gorillas'),
(16411, 'HannaBarbera Super TV Heroes'),
(1261, 'Harvey Hits'),
(12579, 'Howdy Doody'),
(12646, 'Jughead'),
(13668, 'Lidsville'),
(11940, 'Life With Archie'),
(12367, 'Little Audrey TV Funtime'),
(873, 'Lone Ranger''s Famous Horse Hi-Yo Silver'),
(1426, 'SpaceWar'),
(371, 'Sparkling Stars'),
(1822, 'Star Trek'),
(12377, 'Submarine Attack'),
(314, 'Supersnipe Comics'),
(1733, 'TeenTitans'),
(15951, 'Tick'),
(1938, 'Astonishing Tales'),
(2025, 'Demon'),
(1572, 'Fantastic Four Annual'),
(1515, 'Incredible Hulk'),
(1996, 'Special Marvel Edition'),
(1875, 'Tales of Asgard'),
(2118, 'Dracula Lives'),
(19240, 'IDream of Jeannie'),
(11552, 'All Star Comics'),
(13990, 'Humbug'),
(19887, 'threed Love'),
(776, 'Movie Love'),
(2059, 'Night Nurse'),
(11476, 'Romantic Secrets'),
(14115, 'Time for Love'),
(1555, 'Young Love'),
(1021, 'Congo Bill'),
(277, 'Wonder Woman'),
(1067, 'Commander Battle and the Atomic Sub'),
(15029, 'First Love Illustrated'),
(11644, 'Frogman Comics'),
(1624, 'Seargent Rock''s Prize Battle Tales'),
(748, 'War Comics'),
(763, 'Weird Fantasy'),
(1983, 'Weird War Tales'),
(289, 'America''s Best Comics'),
(285, 'Archie Comics'),
(12839, 'Ben Bowie and His Mountain Men'),
(1614, 'Blue Beetle'),
(16743, 'Date with Danger'),
(13876, 'Family Affair'),
(160, 'Fight Comics'),
(11751, 'Gentle Ben'),
(11764, 'Gunsmoke'),
(334, 'Headline Comics'),
(797, 'Indian Chief'),
(2250, 'Inhumans'),
(1562, 'McHale''s Navy'),
(349, 'Mystery Comics'),
(1171, 'Poppo of the Popcorn Theatre'),
(1479, 'Tales Calculated to Drive You Bats'),
(12302, 'Tales Calculated to Drive You Bats'),
(11380, 'Unusual Tales'),
(805, 'Warfront'),
(1063, 'Panic'),
(12404, 'Vault of Horror'),
(764, 'Weird Science'),
(1278, 'Navy Tales'),
(915, 'Out of the Night'),
(941, 'Weird Tales of the Future'),
(31865, 'Dracula'),
(2106, 'Shazam!'),
(760, 'Crypt of Terror'),
(11414, 'Great Gazoo'),
(2400, 'Logan''s Run'),
(2032, 'Secrets of Sinister House'),
(2547, 'Black Hole'),
(15050, 'Man O'' Mars'),
(11363, 'Bobby Sherman'),
(1467, 'Gorgo'),
(1229, 'Nick Haliday'),
(1551, 'Return of Gorgo'),
(12533, 'Underdog'),
(10090, 'Mad Follies'),
(458, 'Real Fact Comics'),
(11942, 'Pink Panther'),
(111, 'Jumbo Comics'),
(1525, 'Boris Karloff Tales of Mystery'),
(1918, 'Dark Shadows'),
(2069, 'Grimm''s Ghost Stories'),
(2087, 'Haunted Love'),
(2140, 'Occult Files of Dr. Spektor'),
(1536, 'SpaceFamily Robinson'),
(1508, 'SpaceMan'),
(12532, 'UFO & Outer Space'),
(2039, 'Weird Western Tales'),
(2038, 'Weird Mystery Tales'),
(2091, 'Black Magic'),
(18203, 'Collected Cheech Wizard'),
(10766, 'Classics Illustrated Junior'),
(11767, 'Hogan''s Heroes'),
(1650, 'Lone Ranger'),
(1652, 'Mighty Samson'),
(2034, 'Swamp Thing'),
(47506, 'Poison Elves Fan Edition'),
(2231, 'Adventures on the Planet of the Apes'),
(1934, 'SuperDCGiant'),
(1900, 'From Beyond the Unknown'),
(594, 'Crime Patrol'),
(2373, 'Bionic Woman'),
(11634, 'Flying Nun'),
(1692, 'Blazing Combat'),
(2947, 'Femforce Special'),
(1638, 'Herbie'),
(1744, 'Fantasy Masterpieces'),
(1686, 'Marvel Collectors'' Item Classics'),
(1907, 'Chamber of Darkness'),
(1750, 'ThorAnnual'),
(1685, 'Journey into MysteryAnnual'),
(1986, 'Captain America Annual'),
(15597, 'Hooded Menace'),
(16728, 'Public Enemies'),
(880, 'Web of Evil'),
(12690, 'Love Confessions'),
(192, 'RedRyder Comics'),
(2187, 'Savage Sword Of Conan'),
(709, 'Buccaneers'),
(386, 'Captain Flight Comics'),
(13996, 'Confessions of Love'),
(379, 'Contact Comics'),
(13419, 'Criminals on the Run'),
(311, 'fourmost'),
(13198, 'Frisky Animals'),
(1973, 'Ghostly Haunts'),
(1723, 'Ghostly Tales'),
(2154, 'SupermanFamily'),
(335, 'Suspense Comics'),
(669, 'Suspense'),
(13397, 'Guns Against Gangsters'),
(19483, 'Law Against Crime'),
(13832, 'Shock Detective Cases'),
(12669, 'Shocking Mystery Cases'),
(10284, 'Spook'),
(15926, 'Startling Terror Tales'),
(874, 'Mickey Mouse'),
(1962, 'Walt Disney Showcase'),
(11127, 'Dennis The Menace'),
(12364, 'Little Lotta Foodland'),
(14577, 'Looney Tunes'),
(7240, 'Beep Beep The Road Runner'),
(2279, 'Tragg and the Sky Gods'),
(7323, 'Tweety and Sylvester'),
(2139, 'Daisy and Donald'),
(15888, 'Wendy Witch World'),
(15886, 'Wendy the Good Little Witch'),
(2138, 'Adam-12'),
(2825, 'Atomic Mouse'),
(6993, 'Bugs Bunny'),
(11708, 'Casper Strange Ghost Stories'),
(562, 'Crime Exposed'),
(12639, 'Porky Pig'),
(2540, 'Legion of Super-Heroes'),
(100, 'Amazing Mystery Funnies'),
(1004, 'Three Stooges'),
(780, 'Amazing Adventures'),
(4049, 'Spider-Man'),
(423, 'Marvel Family'),
(15031, 'My Confessions'),
(7382, 'Famous Crimes'),
(13833, 'Horrors'),
(946, 'Ghostly Weird Stories'),
(16825, 'Holiday Comics'),
(947, 'Terrifying Tales'),
(40908, 'Common Types of Barflyze'),
(11714, 'Crime Fighting Detective'),
(17659, 'Eagle Comics'),
(18286, 'Great Comics'),
(16831, 'Mighty Bear'),
(16832, 'Popular Teen-Agers'),
(19890, 'Ship Ahoy'),
(75651, 'Taffy Comics'),
(16839, 'Top Love Stories'),
(905, 'War Adventures'),
(812, 'Battlefield'),
(1933, 'Hot Wheels'),
(79487, 'Marvel Comics Super Special'),
(6024, 'Captain America: The Classic Years'),
(660, 'My Own Romance'),
(18631, 'Seven Seas Comics'),
(774, 'Captain Science'),
(1673, 'Bewitched'),
(761, 'Tales from the Crypt'),
(15471, 'Outlaws'),
(15822, 'Rat Patrol'),
(12433, 'Supercar'),
(719, 'Flash Gordon'),
(10289, 'Strange Terrors'),
(7396, 'Murder Incorporated'),
(7404, 'My Love Affair'),
(7397, 'Murder Incorporated'),
(892, 'Battle Action'),
(12681, 'Calling All Boys'),
(7394, 'March of Crime'),
(27365, 'Gumps'),
(50126, 'Keeping up with the Joneses'),
(2386, 'Unknown Soldier'),
(542, 'Roy Rogers Comics'),
(12356, 'My Romantic Adventures'),
(818, 'Mystic'),
(1694, 'Daniel Boone'),
(263, 'Punch Comics'),
(128, 'Fantastic Comics'),
(253, 'Air Fighters Comics'),
(169, 'Thrilling Comics'),
(2048, 'Defenders'),
(19564, 'Adventures of Mighty Mouse'),
(958, 'Beetle Bailey'),
(1298, 'Comic Album'),
(1309, 'Cosmo The Merry Martian'),
(15396, 'Kiddie Karnival'),
(13265, 'Laugh'),
(18562, 'Little Audrey'),
(644, 'Little Lizzie'),
(539, 'Marge''s Little Lulu'),
(13476, 'Mighty Mouse'),
(281, 'New Funnies'),
(12488, 'Paul Terry''s comics'),
(541, 'Popeye'),
(13300, 'Rags Rabbit'),
(14931, 'Spooky'),
(60979, 'Help!'),
(1807, 'Avengers Annual'),
(214, 'Star Spangled Comics'),
(12357, 'Little Dot'),
(7213, 'Journey Into Fear'),
(468, 'Zoot Comics'),
(1982, 'Sinister House of Secret Love'),
(14331, 'Lash Larue Western'),
(784, 'Haunt of Fear'),
(4053, 'Thanos Quest'),
(3495, 'Gladstone Comic Album'),
(2325, 'Four Star Spectacular'),
(2104, 'Secret Origins'),
(4667, 'twentyninetynine Unlimited'),
(18767, 'threeDAlienterror'),
(11924, 'Adolescent Radioactive Black Belt Hamsters'),
(18406, 'Adolescent Radioactive Black Belt Hamsters 3-D'),
(3240, 'Adventures Of Captain Jack'),
(14724, 'Adventures Of Ford Fairlane'),
(3345, 'Adventures Of Superman'),
(3220, 'Airboy'),
(3636, 'Akira'),
(3403, 'Alien Legion'),
(2737, 'Alpha Flight'),
(4372, 'Ambush Bug Nothing Special'),
(3567, 'Animal Man'),
(3174, 'Animax'),
(3241, 'Anything Goes!'),
(4183, 'Aquaman'),
(14727, 'Avatar'),
(3829, 'Avengers Spotlight'),
(3747, 'Bad Company'),
(2783, 'Badger'),
(18777, 'Barbaric Tales'),
(4374, 'Batman Adventures'),
(4376, 'Batman Gallery'),
(11210, 'Batman: Catwoman Defiant'),
(4379, 'Batman: Penguin Triumphant'),
(4382, 'Batman: Shadow Of The Bat'),
(4385, 'Black Condor'),
(3573, 'Black Orchid'),
(3574, 'Blackhawk'),
(11504, 'Bloodstrike'),
(3142, 'Blue Beetle'),
(2832, 'Blue Devil'),
(4347, 'Bone'),
(3300, 'Boris The Bear'),
(2092, 'Boy Commandos'),
(12210, 'Brigade'),
(4675, 'Cable'),
(4441, 'Cage'),
(3546, 'Captain Thunder And Blue Bolt'),
(16032, 'Cerebus Bi-Weekly'),
(4191, 'Challengers Of The Unknown'),
(3547, 'Champions'),
(3577, 'Checkmate'),
(3917, 'Cheval Noir'),
(3834, 'Clive Barker''s Hellraiser'),
(16702, 'Coda'),
(3456, 'Contractors'),
(3581, 'Cosmic Odyssey'),
(15367, 'Critical Error'),
(2919, 'Crossfire'),
(14377, 'Cyberforce'),
(3299, 'Daffy Qaddafi'),
(4532, 'Dark Horse Comics'),
(77780, 'Dark Horse Insider'),
(4867, 'Darker Image'),
(4236, 'Darkhawk'),
(7843, 'Darkstars'),
(2596, 'Dazzler'),
(4237, 'Deadly Foes Of Spider-Man'),
(15014, 'Death Crazed Teenage Superheroes'),
(4868, 'Deathblow'),
(4869, 'Deathmate'),
(2931, 'Demon Dreams'),
(3981, 'Demon'),
(17395, 'Dinosaurs For Hire'),
(4586, 'Doc Savage: Devil''s Thoughts'),
(4342, 'Doc Savage: Doom Dynasty'),
(15163, 'Doctor Chaos'),
(3586, 'DoctorFate'),
(21988, 'Dog Boy'),
(4393, 'Doom Force Special'),
(3353, 'Doom Patrol'),
(3244, 'Doomsday Squad'),
(3589, 'Dragonlance'),
(7834, 'Dragonring'),
(3263, 'Dynamo Joe'),
(17638, 'Eagle'),
(7146, 'Echo Of Futurepast'),
(4394, 'Eclipso'),
(3146, 'Electric Warrior'),
(2951, 'Elementals'),
(3899, 'Elementals'),
(40222, 'Elf Warrior'),
(14653, 'ElfLord'),
(13414, 'Enigma'),
(13584, 'Eradicators'),
(3225, 'Espers'),
(3789, 'Etc'),
(4490, 'Eternal Warrior'),
(3287, 'Eternity Smith'),
(15297, 'Evangeline'),
(15191, 'Evangeline Special'),
(2955, 'Evangeline'),
(3307, 'Ex-Mutants'),
(3648, 'Excalibur'),
(13733, 'Excalibur: Air Apparent'),
(4841, 'Exiles'),
(13725, 'Fat Ninja'),
(4843, 'Firearm'),
(11095, 'Fish Police'),
(11098, 'Fish Police Special'),
(3358, 'Flash'),
(3359, 'Flash Annual'),
(3245, 'Flesh And Bones'),
(3790, 'Forgotten Realms'),
(4844, 'Freex'),
(7320, 'Fusion'),
(3184, 'GiJoe Order of Battle'),
(3185, 'GiJoe Special Missions'),
(4025, 'Ghost Rider'),
(15568, 'Gizmo'),
(11143, 'Gotham Nights'),
(3594, 'Green Arrow'),
(3595, 'Green Arrow Annual'),
(3929, 'Green Hornet'),
(3148, 'Green Lantern Corps'),
(4400, 'Green Lantern Corps Quarterly'),
(3986, 'Green Hornet'),
(4402, 'Green Lantern: Mosaic'),
(3255, 'Grendel'),
(40720, 'Grey'),
(4026, 'Guardians Of The Galaxy'),
(17301, 'Gyro Force'),
(4491, 'HARDCorps'),
(3270, 'Hamster Vice'),
(4847, 'Hardcase'),
(2745, 'Hawkeye'),
(3988, 'Hawkworld'),
(3598, 'Haywire'),
(4454, 'Hell''s Angel'),
(3599, 'Hellblazer'),
(9831, 'Hellstorm: Prince Of Lies'),
(4307, 'Herbie'),
(3521, 'Hero Sandwich'),
(2979, 'Hex'),
(21079, 'Holiday Out'),
(3802, 'Huntress'),
(20328, 'Jack Hunter'),
(4199, 'Jaguar'),
(3718, 'Jezebel Jade'),
(4539, 'John Byrne''s Next Men'),
(3257, 'Jonny Quest'),
(2809, 'Judge Dredd'),
(3339, 'Judge Dredd V2'),
(3190, 'Justice'),
(3364, 'Justice League'),
(3805, 'Justice League Europe'),
(10453, 'Justice League Quarterly'),
(14155, 'Justice Machine'),
(4407, 'Justice Society of America'),
(40721, 'Justy'),
(2600, 'KaZarTheSavage'),
(16818, 'Kamui'),
(19180, 'Laffin'' Gas'),
(3079, 'Laser Eraser And Pressbutton'),
(4031, 'Last American'),
(15150, 'Last Of The Viking Heroes'),
(26333, 'Legacy'),
(4202, 'Legend Of The Shield'),
(3810, 'Legion Of Super-Heroes'),
(32260, 'Libby Ellis'),
(14710, 'Lobo: Portrait Of A Victim'),
(10081, 'Lone Wolf And Cub'),
(5113, 'Madman Comics'),
(4255, 'Magnus Robot Fighter'),
(2459, 'Man From Atlantis'),
(14043, 'Man Of Rust'),
(21067, 'Manimal'),
(4849, 'Mantra'),
(3194, 'Mark Hazzard: Merc'),
(10079, 'Marshal Law'),
(3654, 'Marvel Comics Presents'),
(2657, 'Marvel Fanfare'),
(2259, 'Marvel Presents'),
(1911, 'Marvels Greatest Comics'),
(19505, 'Masques'),
(3196, 'Masters Of The Universe'),
(4872, 'Maxx'),
(27545, 'Mecha'),
(16043, 'Miami Mice'),
(2514, 'Micronauts'),
(16087, 'Midnite Skulker'),
(20718, 'Mighty Mites'),
(3080, 'Miracleman'),
(2562, 'Moon Knight'),
(3031, 'Moon Knight'),
(3032, 'Moonshadow'),
(4461, 'Morbius: The Living Vampire'),
(45136, 'Neomen'),
(3082, 'New DNAgents'),
(11333, 'New Gods'),
(16073, 'New Humans'),
(2755, 'New Mutants'),
(7065, 'New Teen Titansv2 Annual'),
(3228, 'New Wave'),
(48598, 'New World Order'),
(16520, 'Next Man'),
(2784, 'Nexus'),
(4851, 'Night Man'),
(3198, 'Nightmask'),
(14579, 'Ninja High School'),
(4466, 'Nomad'),
(14018, 'Official Crisis On Infinite Earths Index'),
(21070, 'Open Season'),
(20334, 'Outposts'),
(2687, 'Pacific Presents'),
(15083, 'Paul The SamuraiV2'),
(4467, 'Pendragon'),
(7470, 'Phaze'),
(7471, 'Pineapple Army'),
(4873, 'Pitt'),
(13760, 'Planet Of The Apes'),
(40557, 'Power and Glory'),
(2886, 'Power Pack'),
(3273, 'PreTeen Dirty-Gene Kung-Fu kangaroos'),
(14288, 'Primer'),
(4853, 'Prototype'),
(3465, 'Prowler'),
(3293, 'Puma Blues'),
(3431, 'Punisher'),
(4724, 'Punisher Twentyninetynine'),
(3662, 'Punisher War Journal'),
(4042, 'Punisher No Escape'),
(3857, 'Quasar'),
(3998, 'Question Quarterly'),
(2888, 'Questprobe'),
(14523, 'Ragman'),
(4493, 'Rai'),
(14966, 'Realm'),
(18036, 'Redfox'),
(4472, 'Ren & Stimpy Show'),
(3696, 'Revenge Of The Prowler'),
(7993, 'Roachmill'),
(16975, 'Robo-Hunter'),
(4046, 'Robocop'),
(20845, 'Robot Comics'),
(11693, 'Robotech Masters'),
(2516, 'Rom'),
(5143, 'Rune'),
(13856, 'Rust'),
(13857, 'Rust'),
(25979, 'Rust'),
(49780, 'STAT'),
(4727, 'Sabretooth'),
(14659, 'Samurai'),
(18007, 'Samurai Penguin'),
(3817, 'Sandman'),
(4874, 'Savage Dragon'),
(3748, 'Scavengers'),
(16336, 'Scavengers'),
(3085, 'Scout'),
(3467, 'Scout Handbook'),
(3698, 'Scout: War Shaman'),
(3305, 'Seadragon'),
(32217, 'Second City'),
(4758, 'Second Life Of Doctor Mirage'),
(3166, 'Secret Origins'),
(4759, 'Secret Weapons'),
(3858, 'Sensational She-Hulk'),
(3379, 'Shadow'),
(3378, 'Shadow Annual'),
(4494, 'Shadowman'),
(16104, 'Shatter'),
(17625, 'Shock Therapy'),
(14030, 'Shuriken'),
(3433, 'Silver Surfer'),
(3512, 'Slaine The Berserker'),
(4249, 'Sleepwalker'),
(3860, 'Sleeze Brothers'),
(4854, 'Sludge'),
(4856, 'Solution'),
(47180, 'Soul Trek'),
(18013, 'SpaceArk'),
(3749, 'Speed Racer Special'),
(3325, 'Spellbinders'),
(4477, 'Spider-ManTwentyninetynine'),
(3203, 'Spitfire And The Troubleshooters'),
(26119, 'Splat!'),
(3671, 'SaintGeorge'),
(3204, 'Star Brand'),
(3823, 'Star Trek'),
(3825, 'Star Trek: The Next Generation'),
(14662, 'Stark: Future'),
(2690, 'Starslayer'),
(4879, 'Stormwatch'),
(4858, 'Strangers'),
(21074, 'Strata'),
(20311, 'Street Wolf'),
(3206, 'Strikeforce: Morituri'),
(40175, 'Stygmata'),
(4002, 'Superboy'),
(4417, 'SupermanSpecial'),
(3386, 'Superman2'),
(4215, 'SupermanTheManOfSteel'),
(4612, 'Supreme'),
(13888, 'Syphons'),
(14148, 'Tales of Terror'),
(12258, 'Tales of the Green Hornet'),
(2850, 'Tales Of The Legion Of Super-Heroes'),
(3878, 'Tapping The Vein'),
(3700, 'Target: Airboy'),
(10096, 'Team Titans'),
(16590, 'Ted Mckeever''s Metropol'),
(3171, 'TeenTitans Spotlight'),
(13912, 'TeenageMutant Ninja Turtles'),
(17138, 'Terminator'),
(3701, 'Total Eclipse'),
(2898, 'Transformers'),
(7844, 'Tribe'),
(49693, 'Triumphant Unleashed'),
(16708, 'Trollords'),
(56547, 'Trouble With Girls'),
(4006, 'Twilight'),
(3306, 'Twilight Avenger'),
(19616, 'Ultra Klutz'),
(4882, 'Union'),
(3003, 'V'),
(4761, 'Valiant Reader'),
(19764, 'Vector'),
(16397, 'Vengeance Squad'),
(4294, 'Venus Wars'),
(11034, 'Vertigo Preview'),
(27460, 'Vic And Blood'),
(3441, 'Video Jack'),
(16815, 'Vintage Magnus Robot Fighter'),
(4481, 'Warheads'),
(4482, 'Warlock'),
(4483, 'Warlock And The Infinity Watch'),
(13977, 'Warriors Of Plasm'),
(3391, 'Wasteland'),
(4217, 'Web'),
(3059, 'Web Of Spider-Man'),
(3060, 'Web Of Spider-Man Annual'),
(3111, 'Whisper Special'),
(3266, 'Whisper'),
(3235, 'Whodunnit?'),
(13483, 'WildC.A.T.S Trilogy'),
(4883, 'Wildstar: Sky Zero'),
(4770, 'Wildthing'),
(3396, 'Wonder Woman'),
(4009, 'World''s Finest'),
(3210, 'X-Factor Annual'),
(4253, 'X-Force'),
(4488, 'X-MenAdventures'),
(4254, 'X-Men2'),
(3678, 'X-Terminators'),
(10741, 'Young Indiana Jones Chronicles'),
(12225, 'Youngblood'),
(4607, 'Zombie War'),
(3865, 'Wolverine 2'),
(4252, 'Wonder Man'),
(13121, 'ninteeneightyfour'),
(12308, 'Bone Holiday Special'),
(12211, 'Brigade'),
(1621, 'CaptainStorm'),
(39840, 'Daemonstorm'),
(2233, 'Doc Savage'),
(2162, 'Doctor Strange'),
(5343, 'Elementals'),
(5857, 'Flaming Carrot Comics Annual'),
(7152, 'Frank Frazetta Fantasy Illustrated'),
(15676, 'Frontline Combat Reprints'),
(19117, 'Ghetto Blasters'),
(43489, 'Grunts'),
(1675, 'Guerrilla War'),
(11406, 'Jetsons'),
(7456, 'Knights on Broadway'),
(2123, 'Marvel Double Feature'),
(2124, 'Marvel Spectacular'),
(38041, 'Monster Hunters'),
(2633, 'Night Force'),
(13530, 'Official Marvel Index to the X-Men'),
(40544, 'Pantera'),
(164, 'Pep Comics'),
(31556, 'Radical Dreamer'),
(12227, 'Roarin'' Rick''s Rare Bit Fiends'),
(1821, 'Scamp'),
(11389, 'Secret Romance'),
(4610, 'Shadowhawk'),
(5587, 'Speed Demon'),
(2564, 'Star Trek'),
(5560, 'Star TrekDeep Space Nine'),
(4485, 'Tekworld'),
(5217, 'Telluria'),
(14131, 'Thieves & Kings'),
(21636, 'Thrax'),
(2897, 'Timespirits'),
(11496, 'Top Eliminator'),
(41107, 'Warrior'),
(1792, 'World of Wheels'),
(7517, 'X-Files'),
(12505, 'Archie''s Madhouse'),
(11354, 'Barney and Betty Rubble'),
(6139, 'Batman: Dark Victory'),
(2805, 'Captain Paragon'),
(16034, 'Cerebus Church & State'),
(3070, 'Cerebus Jam'),
(19012, 'Courtship of Eddie''s Father'),
(23588, 'Crazy Magazine'),
(1566, 'Devil Kids Starring Hot Stuff'),
(20129, 'Exquisite Corpse'),
(13667, 'Fat Albert'),
(1788, 'Grand Prix'),
(19655, 'Haunted Horseman'),
(11409, 'Hong Kong Phooey'),
(12428, 'Little Sad Sack'),
(11402, 'Love Diary'),
(2908, 'Megaton Man'),
(13510, 'Mod Wheels'),
(25467, 'Monster Massacre'),
(16715, 'Nash Preview Book'),
(45508, 'Purgatori: The Dracula Gambit'),
(6256, 'Rising Stars'),
(11391, 'Secrets of Young Brides'),
(14108, 'Speed Buggy'),
(10394, 'Stray Bullets'),
(1603, 'SuperGoof'),
(48602, 'Twister'),
(11565, 'Baby Huey and Papa'),
(2215, 'Claw the Unconquered'),
(2508, 'Fantasy Masterpieces'),
(17695, 'Happy Rabbit'),
(2586, 'Madame Xanadu'),
(11467, 'Sweethearts'),
(2230, 'Tor'),
(2858, 'Alien Legion'),
(2506, 'Amazing Adventures'),
(1080, 'Black Fury'),
(17711, 'Black Kiss'),
(4014, 'Cadillacs and Dinosaurs'),
(2371, 'Captain Britain'),
(553, 'Desperado'),
(2441, 'Doorway to Nightmare'),
(2346, 'Eternals'),
(1500, 'Ghost Stories'),
(18929, 'Gil Thorp'),
(1789, 'Hercules'),
(1236, 'Jerry Drummer'),
(2052, 'Journey Into Mystery'),
(1894, 'Jungle Jim'),
(2257, 'Marvel Feature'),
(18009, 'Maze Agency'),
(19181, 'Megaton'),
(2206, 'Monster Hunters'),
(23560, 'Jungle Jimo'),
(40715, 'Jungle Jimo Annual'),
(12640, 'Porky Pig'),
(3114, 'Revengers Featuring Megalith'),
(22430, 'Rocky Lane Western Reprints'),
(2224, 'Secrets of Haunted House'),
(18554, 'Slaughterman'),
(18083, 'Smokey Bear'),
(3384, 'Spectre'),
(2188, 'Spidey Super Stories'),
(11471, 'Strange Suspense Stories'),
(13868, 'Toyboy'),
(2065, 'Werewolf By Night'),
(1950, 'Where Monsters Dwell'),
(17090, 'Zen Intergalactic Ninja'),
(12549, 'Angel'),
(18290, 'Apache Trail'),
(2008, 'Bravados'),
(2117, 'Dead of Night'),
(16704, 'Hair Bear Bunch'),
(12520, 'Informer'),
(2329, 'Karate Kid'),
(13075, 'Silver Kid Western'),
(2794, 'Silver Star'),
(15831, 'Steve Canyon'),
(1804, 'THECat'),
(2135, 'Weird Wonder Tales'),
(1138, 'Wyatt Earp'),
(2651, 'Fantastic Four Roast'),
(4734, 'Spider-Man Unlimited'),
(4740, 'Thor Corps'),
(1729, 'Plastic Man'),
(11968, 'Betty'),
(20774, 'Brave And The Bold Annual'),
(2842, 'New Teen Titansv2'),
(4752, 'X-Mentwentyninetynine'),
(1640, 'Creepy'),
(23151, 'Devilman'),
(62768, 'Betty Page in Jungleland'),
(698, 'Girls'' Romances'),
(13464, 'Romantic Story'),
(1108, 'Dell Junior Treasury'),
(12412, 'Sad Sack and the Sarge'),
(10515, 'True Love Problems and Advice Illustrated'),
(2097, 'GIWar Tales'),
(4145, 'Spac Funnies'),
(12510, 'Fantastic Voyage'),
(3086, 'Seduction Of The Innocent'),
(2507, 'Battlestar Galactica'),
(2214, 'Beowulf'),
(8018, 'Brothers of the Spear'),
(2232, 'Champions'),
(2072, 'Dagar the Invincible'),
(2040, 'Weird Worlds'),
(2515, 'Micronauts Annual'),
(2404, 'RedSonja'),
(2398, 'John Carter Warlord Of Mars'),
(17128, 'XYZ Comics'),
(11408, 'Huckleberry Hound'),
(11101, 'Lost In Space'),
(4972, 'Steel'),
(37835, 'Lander'),
(66430, 'Mask of Zorro'),
(13666, 'ILove You'),
(3233, 'True Love'),
(11451, 'High School Confidential Diary'),
(1972, 'Ghost Manor'),
(11385, 'Yogi Bear'),
(10516, 'Gargoyles'),
(12362, 'Little Lotta'),
(12418, 'Sad Sack Laugh Special'),
(2363, 'Gold Key Spotlight'),
(1819, 'Moby Duck'),
(12924, 'Walter Lantz Andy Panda'),
(24829, 'Weird Science'),
(24916, 'Crime SuspenStories'),
(26447, 'Phantom'),
(4179, 'Dick Tracy'),
(16482, 'Ralph Snart Adventures'),
(13754, 'Lancelot Link, Secret Chimp'),
(16484, 'Ralph Snart Adventures'),
(15733, 'Pink Panther'),
(15469, 'Anne Rice''s Interview With The Vampire'),
(2691, 'Twisted Tales'),
(2070, 'Jungle Twins'),
(11412, 'Hee Haw'),
(19013, 'Felix the Cat'),
(12426, 'Sad Sad Sack World'),
(3584, 'Detective Comics Annual'),
(13775, 'Land Of The Giants'),
(2829, 'Atari Force'),
(3139, 'Atari Force Special'),
(1549, 'Army War Heroes'),
(11357, 'Battlefield Action'),
(1176, 'Fightin'' Army'),
(2381, 'Seargent Rock'),
(3617, 'Seargent Rock Special'),
(11757, 'Adventures of Big Boy'),
(12842, 'Henry Aldrich'),
(2714, 'Batman and the Outsiders'),
(2835, 'Legion Of Super-Heroes');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
