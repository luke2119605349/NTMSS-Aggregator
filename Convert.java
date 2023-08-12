package conversion;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import bo.Manuscript;
import bo.ManuscriptVerse;
import bo.Verse;
import dataaccesslayer.HibernateUtil;

public class Convert {
	public static ArrayList<String> books = new ArrayList<String>(Arrays.asList(
		"matthew",
		"mark",
		"luke",
		"john",
		"acts",
		"romans",
		"1corinthians",
		"2corinthians",
		"galatians",
		"ephesians",
		"philippians",
		"colossians",
		"1thessalonians",
		"2thessalonians",
		"1timothy",
		"2timothy",
		"titus",
		"philemon",
		"hebrews",
		"james",
		"1peter",
		"2peter",
		"1john",
		"2john",
		"3john",
		"jude",
		"revelation"
	));
	
	static Map<String, Integer> firstBook = new HashMap<String,Integer>(Map.of(
			"gospels", 1,
			"paulineepistles", 6,
			"generalepistles", 19,
			"newtestament", 1));
	
	static Map<String, Integer> lastBook = new HashMap<String,Integer>(Map.of(
			"gospels", 4,
			"paulineepistles", 18,
			"generalepistles", 26,
			"newtestament",27));
	
	static Map<String, String> aliases;
	
	public static Map<String, ArrayList<Integer>> structure;
		
	private static void populateAliases() {
		aliases = new HashMap<String,String>();
		aliases.put("matt", "matthew");
		aliases.put("mt", "matthew");
		aliases.put("mk", "mark");
		aliases.put("luk", "luke");
		aliases.put("lk", "luke");
		aliases.put("jn", "john");
		aliases.put("rom", "romans");
		aliases.put("1cor", "1corinthians");
		aliases.put("2cor", "2corinthians");
		aliases.put("gal", "galatians");
		aliases.put("eph", "ephesians");
		aliases.put("phil", "philippians");
		aliases.put("col", "colossians");
		aliases.put("1thess", "1thessalonians");
		aliases.put("2thess", "2thessalonians");
		aliases.put("2the", "2thessalonians");
		aliases.put("1tim", "1timothy");
		aliases.put("2tim", "2timothy");
		aliases.put("tit", "titus");
		aliases.put("phlm", "philemon");
		aliases.put("heb", "hebrews");
		aliases.put("jas", "james");
		aliases.put("1pet", "1peter");
		aliases.put("1pe", "1peter");
		aliases.put("2pet", "2peter");
		aliases.put("2pe", "2peter");
		aliases.put("1jn", "1john");
		aliases.put("2jn", "2john");
		aliases.put("3jn", "3john");
		aliases.put("jd", "jude");
		aliases.put("rev", "revelation");
	}
	
	public static void populateStructure() {
		structure = new HashMap<String, ArrayList<Integer>>();
		structure.put("matthew", new ArrayList<Integer>(Arrays.asList(25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20)));
		structure.put("mark", new ArrayList<Integer>(Arrays.asList(45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20)));
		structure.put("luke", new ArrayList<Integer>(Arrays.asList(80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53)));
		structure.put("john", new ArrayList<Integer>(Arrays.asList(51,25,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25)));
		structure.put("acts", new ArrayList<Integer>(Arrays.asList(26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31)));
		structure.put("romans", new ArrayList<Integer>(Arrays.asList(32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27)));
		structure.put("1corinthians", new ArrayList<Integer>(Arrays.asList(31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24)));
		structure.put("2corinthians", new ArrayList<Integer>(Arrays.asList(24,17,18,18,21,18,16,24,15,18,33,21,14)));
		structure.put("galatians", new ArrayList<Integer>(Arrays.asList(24,21,29,31,26,18)));
		structure.put("ephesians", new ArrayList<Integer>(Arrays.asList(23,22,21,32,33,24)));
		structure.put("philippians", new ArrayList<Integer>(Arrays.asList(30,30,21,23)));
		structure.put("colossians", new ArrayList<Integer>(Arrays.asList(29,23,25,18)));
		structure.put("1thessalonians", new ArrayList<Integer>(Arrays.asList(10,20,13,18,28)));
		structure.put("2thessalonians", new ArrayList<Integer>(Arrays.asList(12,17,18)));
		structure.put("1timothy", new ArrayList<Integer>(Arrays.asList(20,15,16,16,25,21)));
		structure.put("2timothy", new ArrayList<Integer>(Arrays.asList(18,26,17,22)));
		structure.put("titus", new ArrayList<Integer>(Arrays.asList(16,15,15)));
		structure.put("philemon", new ArrayList<Integer>(Arrays.asList(25)));
		structure.put("hebrews", new ArrayList<Integer>(Arrays.asList(14,18,19,16,14,20,28,13,28,39,40,29,25)));
		structure.put("james", new ArrayList<Integer>(Arrays.asList(27,26,18,17,20)));
		structure.put("1peter", new ArrayList<Integer>(Arrays.asList(25,25,22,19,14)));
		structure.put("2peter", new ArrayList<Integer>(Arrays.asList(21,22,18)));
		structure.put("1john", new ArrayList<Integer>(Arrays.asList(10,29,24,21,21)));
		structure.put("2john", new ArrayList<Integer>(Arrays.asList(13)));
		structure.put("3john", new ArrayList<Integer>(Arrays.asList(14)));
		structure.put("jude", new ArrayList<Integer>(Arrays.asList(25)));
		structure.put("revelation", new ArrayList<Integer> (Arrays.asList(20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21)));
	};
	
	private static final int lastAlpha(String s) {
	    for (int i = s.length() - 1; i >= 0; i--) {
	        char c = s.charAt(i);
	        if (Character.isLetter(c))
	            return i;
	    }
	    return -1; // no alphanumeric character at all
	}
	
	private static final String standardize(String book) {
		book = book.toLowerCase();
		if (aliases.containsKey(book)) {
			book = aliases.get(book);
		}
		return book;
	}
	
	private static final ArrayList<Integer> lastOf(Integer book, Integer chapter, Integer verse) {
		if (chapter == null) {
			chapter = structure.get(BibleRange.bookName(book)).size();
		}
		if (verse == null) {
			verse = structure.get(BibleRange.bookName(book)).get(chapter-1);
		}
		
		return new ArrayList<Integer>(Arrays.asList(book, chapter, verse));
	}
	
	private static ArrayList<BibleRange> parseContents(String contents) {
		ArrayList<BibleRange> bibleRanges = new ArrayList<>();
		
		try {
			String[] ranges = contents.replace(" ", "").split(",");
			Integer currBook = null;
			Integer currChapter = null;
			for (String range : ranges) {
				String lhs = range;
				String rhs = "";
				if (range.contains("-")) {
					String[] sides = range.split("-");
					lhs = sides[0];
					rhs = sides[1];
				}
			
				String lhsCollection=null;
				Integer lhsBook=null;
				Integer lhsChapter=null;
				Integer lhsVerse=null;
				boolean isExplicitChapter=false;
				boolean isExplicitVerse=false;
				Integer bookend=null;
				
				int endOfBook = lastAlpha(lhs);
				if (endOfBook < 0) {
					lhsBook = currBook;
				} else {
					lhsCollection = lhs.substring(0, endOfBook+1);
					lhsCollection = standardize(lhsCollection);
					if (books.contains(lhsCollection)) {
						lhsBook = BibleRange.bookIndex(lhsCollection);
					} else if (firstBook.containsKey(lhsCollection)) {
						lhsBook = firstBook.get(lhsCollection);
						bookend = lastBook.get(lhsCollection);
					}
					lhsChapter = 1;
					lhsVerse = 1;
					currBook = lhsBook;
					currChapter = null;
				}
				
				if (endOfBook+1 != lhs.length()) {
					lhs = lhs.substring(endOfBook+1);
					if (lhs.contains(":")) {
						String[] nums = lhs.split(":");
						lhsChapter = Integer.parseInt(nums[0]);
						currChapter = lhsChapter;
						lhsVerse = Integer.parseInt(nums[1]);
						isExplicitChapter = true;
						isExplicitVerse = true;
					} else if (currChapter == null) {
						lhsChapter = Integer.parseInt(lhs);
						isExplicitChapter = true;
						lhsVerse = 1;
						//currChapter = lhsChapter;
					} else {
						isExplicitChapter = true;
						isExplicitVerse = true;
						lhsChapter = currChapter;
						lhsVerse = Integer.parseInt(lhs);
					}
				}
				
				Integer rhsBook=null;
				Integer rhsChapter=null;
				Integer rhsVerse=null;
				if (rhs == "") {
					ArrayList<Integer> ref;
					if (bookend == null) {
						bookend = lhsBook;
					}
					if (isExplicitVerse) {
						ref = lastOf(bookend, lhsChapter, lhsVerse);
					} else if (isExplicitChapter) {
						ref = lastOf(bookend, lhsChapter, null);
					} else {
						ref = lastOf(bookend, null, null);
					}
					rhsBook = ref.get(0);
					rhsChapter = ref.get(1);
					rhsVerse = ref.get(2);
				} else {
					endOfBook = lastAlpha(rhs);
					if (endOfBook < 0) {
						rhsBook = currBook;
					} else {
						String rhsBookName = rhs.substring(0, endOfBook+1);
						rhsBookName = standardize(rhsBookName);
						if (books.contains(rhsBookName)) {
							rhsBook = BibleRange.bookIndex(rhsBookName);
						}
						rhsChapter = 1;
						rhsVerse = 1;
						currBook = rhsBook;
						currChapter = null;
					}
					
					if (endOfBook+1 != rhs.length()) {
						rhs = rhs.substring(endOfBook+1);
						if (rhs.contains(":")) {
							String[] nums = rhs.split(":");
							rhsChapter = Integer.parseInt(nums[0]);
							currChapter = rhsChapter;
							rhsVerse = Integer.parseInt(nums[1]);
						} else if (currChapter == null) {
							rhsChapter = Integer.parseInt(rhs);
							rhsVerse = 1;
							currChapter = rhsChapter;
						} else {
							rhsVerse = Integer.parseInt(rhs);
							rhsChapter = currChapter;
						}
					}
				}
				
				bibleRanges.add(new BibleRange(lhsBook, lhsChapter, lhsVerse, rhsBook, rhsChapter, rhsVerse));
			}
			return bibleRanges;
		} catch (Exception e) {
			return new ArrayList<>();
		}
	};

	static Connection conn;
	static final String MYSQL_CONN_URL = "jdbc:mysql://127.0.0.1:3306/ntmss2";  

	public static void main(String[] args) {
		try {
			populateStructure();
			populateAliases();
			long startTime = System.currentTimeMillis();
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection(MYSQL_CONN_URL, "ntviewer", "tr");
			convert();
			long endTime = System.currentTimeMillis();
			long elapsed = (endTime - startTime) / (1000*60);
			System.out.println("Elapsed time in mins: " + elapsed);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				if (!conn.isClosed()) conn.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		HibernateUtil.stopConnectionProvider();
		HibernateUtil.getSessionFactory().close();
	}

	private static void convert() {
		try {
			HashMap<Verse.VerseId, Verse> verses = getVerses();
			System.out.println("Verses Retrieved.");
			for (Verse v : verses.values()) {
				HibernateUtil.persistVerse(v);
			}
			System.out.println("Persisted Verses.");
			HashMap<Manuscript.ManuscriptId, Manuscript> manuscripts = getManuscripts(verses);
			System.out.println("Manuscripts Retrieved.");
			HibernateUtil.flushObjects();
			HibernateUtil.clearObjects();
			attachLinksToManuscripts(manuscripts);
			System.out.println("Linked Manuscripts.");
			HibernateUtil.flushObjects();
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void attachLinksToManuscripts(
			HashMap<Manuscript.ManuscriptId, Manuscript> manuscripts) {
		try {
			PreparedStatement ps = conn.prepareStatement("select " + 
					"ms_id, " +
					"page, " +
					"contents " +
					"from mslinks " +
					"order by ms_id desc");
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				String ms_id = rs.getString("ms_id");
				String page = rs.getString("page");
				String contents = rs.getString("contents");
				if (ms_id == null	|| ms_id.isEmpty() 
						|| page == null 
						|| page.isEmpty()
						|| contents == null
						|| contents.isEmpty())
					continue;
				Manuscript m = new Manuscript(
						Integer.parseInt(ms_id.substring(0,1)),
						Integer.parseInt(ms_id.substring(1)));
				if (!manuscripts.containsKey(m.getId()))
					continue;
				for (BibleRange br : parseContents(contents)) {
					Verse.VerseId vid = br.getNext();
					while (vid != null) {
						Verse v = new Verse(vid.book, vid.chapter, vid.verse);
						ManuscriptVerse mv = 
								new ManuscriptVerse(m, v);
						HibernateUtil.linkManuscript(mv, Integer.parseInt(page));
						vid = br.getNext();
					}					
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void attachDuplicatesToManuscript(Manuscript manuscript) {
		try {
			PreparedStatement ps = conn.prepareStatement("select " + 
					"ms_copy " +
					"from abs " +
					"where ms_source = ?");
			ps.setInt(1, manuscript.getType()*10000 + manuscript.getName());
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				String duplicate = rs.getString("ms_copy");
				if (duplicate == null 
						|| duplicate.isEmpty()
						|| !manuscript.getType().equals(Integer.parseInt(duplicate.substring(0,1))))
					continue;
				manuscript.addDuplicate(Integer.parseInt(duplicate.substring(1)));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void attachCopiesToManuscript(Manuscript manuscript) {
		try {
			PreparedStatement ps = conn.prepareStatement("select " + 
					"ms_copy " +
					"from ms_is_ms " +
					"where ms_source = ?");
			ps.setInt(1, manuscript.getType()*10000 + manuscript.getName());
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				String copy = rs.getString("ms_copy");
				if (copy == null 
						|| copy.isEmpty()
						|| !manuscript.getType().equals(Integer.parseInt(copy.substring(0,1))))
					continue;
				manuscript.addCopy(Integer.parseInt(copy.substring(1)));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static HashMap<Verse.VerseId, Verse> getVerses() {
		HashMap<Verse.VerseId, Verse> verses = new HashMap<Verse.VerseId, Verse>();
		try {
			PreparedStatement ps = conn.prepareStatement("select " + 
					"reference, " + 
					"text " +
					"from kjvnt");
			ResultSet rs = ps.executeQuery();
			int count=0; // for progress feedback only
			while (rs.next()) {
				count++;
				// this just gives us some progress feedback
				if (count % 1000 == 0)
					System.out.println("num verses: " + count);
				String reference = rs.getString("reference");
				String text = rs.getString("text");
				if (reference == null	|| reference.isEmpty() 
										|| text == null 
										|| text.isEmpty())
					continue;
				Pattern p = Pattern.compile("^(.*) (\\d+):(\\d+)$");
				Matcher m = p.matcher(reference);
				if (!m.matches())
					continue;
				Integer bookNo = BibleRange.bookIndex(standardize(m.group(1).replace(" ", "")));
				Integer chapterNo = Integer.parseInt(m.group(2));
				Integer verseNo = Integer.parseInt(m.group(3));
				Verse v = new Verse(bookNo, chapterNo, verseNo);
				v.setText(text);
				verses.put(v.getId(), v);
			}
			rs.close();
			ps.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return verses;
	}

	public static HashMap<Manuscript.ManuscriptId, Manuscript> getManuscripts(
			HashMap<Verse.VerseId, Verse> verses) {
		HashMap<Manuscript.ManuscriptId, Manuscript> manuscripts = new HashMap<Manuscript.ManuscriptId, Manuscript>();
		ArrayList<String> badManuscriptContents = new ArrayList<String>();
		try {
			PreparedStatement ps = conn.prepareStatement("select " + 
					"ms_id, " + 
					"cent, " +
					"contents " +
					"from ms " +
					"order by ms_id " +
					"limit 140");
			ResultSet rs = ps.executeQuery();
			int count=0; // for progress feedback only
			while (rs.next()) {
				count++;
				// this just gives us some progress feedback
				if (count % 1000 == 0)
					System.out.println("num manuscripts: " + count);
				String midStr = rs.getString("ms_id");
				String centStr = rs.getString("cent");
				String contents = rs.getString("contents");
				if (midStr == null	|| midStr.isEmpty() 
									|| centStr == null 
									|| centStr.isEmpty()
									|| contents == null
									|| contents.isEmpty())
					continue;
				Manuscript manuscript = new Manuscript(
					Integer.parseInt(midStr.substring(0,1)),
					Integer.parseInt(midStr.substring(1))
				);
				Integer c = Integer.parseInt(centStr);
				if (c < 0 || c > 21) {
					continue;
				}
				manuscript.setCentury(c);
				attachDuplicatesToManuscript(manuscript);
				attachCopiesToManuscript(manuscript);
				HibernateUtil.persistManuscript(manuscript);
				for (BibleRange br : parseContents(contents)) {
					Verse.VerseId vid = br.getNext();
					boolean duplicateVerses = false;
					while (vid != null && verses.containsKey(vid)) {
						Verse verse = verses.get(vid);
						ManuscriptVerse manuscriptverse = new ManuscriptVerse(manuscript, verse);
						duplicateVerses = !HibernateUtil.persistManuscriptVerse(manuscriptverse);
						vid = br.getNext();
					}
					if (duplicateVerses) {
						badManuscriptContents.add(midStr);
					}
				}
				manuscripts.put(manuscript.getId(), manuscript);
			}
			rs.close();
			ps.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		System.out.println("Bad Manuscript Contents: [");
		for (String badManuscript : badManuscriptContents) {
			System.out.println("\t" + badManuscript);
		}
		System.out.println("]");
		return manuscripts;
	}
}