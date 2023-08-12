package conversion;

import bo.Verse.VerseId;

public class BibleRange {
	int startBook;
	int startChapter;
	int startVerse;
	int endBook;
	int endChapter;
	int endVerse;
	int currBook;
	int currChapter;
	int currVerse;
	boolean done;
	
	BibleRange(int sb, int sc, int sv, int eb, int ec, int ev) {
		startBook = sb;
		startChapter = sc;
		startVerse = sv;
		endBook = eb;
		endChapter = ec;
		endVerse = ev;
		currBook = sb;
		currChapter = sc;
		currVerse = sv;
		done = false;
	}
	
	public static String bookName(int book) {
		return Convert.books.get(book-1);
	}
	
	public static Integer bookIndex(String book) {
		return Convert.books.indexOf(book)+1;
	}
	VerseId getNext() {
		if (done 
				|| currBook > 27 
				|| currChapter > Convert.structure.get(bookName(currBook)).size()
				|| currVerse > Convert.structure.get(bookName(currBook)).get(currChapter-1)) {
			return null;
		}
		VerseId v = new VerseId();
		v.book = currBook;
		v.chapter = currChapter;
		v.verse = currVerse;
		
		if (currBook == endBook && currChapter == endChapter && currVerse == endVerse) {
			done = true;
		} else {
			if (currVerse == Convert.structure.get(bookName(currBook)).get(currChapter-1)) {
				if (currChapter == Convert.structure.get(bookName(currBook)).size()) {
					currChapter = 1;
					currVerse = 1;
					++currBook;
				} else {
					currVerse = 1;
					++currChapter;
				}
			} else {
				++currVerse;
			}
		}
		
		return v;
	}
}
