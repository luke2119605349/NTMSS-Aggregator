package dataaccesslayer;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.engine.spi.SessionFactoryImplementor;
import org.hibernate.service.spi.Stoppable;

import org.hibernate.engine.jdbc.connections.spi.ConnectionProvider;

import bo.Manuscript;
import bo.ManuscriptVerse;
import bo.Verse;
import conversion.Convert;

import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.AbstractMap.SimpleEntry;

public class HibernateUtil {

	private static final SessionFactory sessionFactory;

	static {
		try {
			Configuration cfg = new Configuration()
				.addAnnotatedClass(bo.Manuscript.class)
				.addAnnotatedClass(bo.ManuscriptVerse.class)
				.addAnnotatedClass(bo.Verse.class)
				.configure();
			StandardServiceRegistryBuilder builder = new StandardServiceRegistryBuilder().
			applySettings(cfg.getProperties());
			sessionFactory = cfg.buildSessionFactory(builder.build());
		} catch (Throwable ex) {
			System.err.println("Initial SessionFactory creation failed." + ex);
			throw new ExceptionInInitializerError(ex);
		}
	}

	public static SessionFactory getSessionFactory() {
		return sessionFactory;
	}
  
	public static void stopConnectionProvider() {
		final SessionFactoryImplementor sessionFactoryImplementor = (SessionFactoryImplementor) sessionFactory;
		@SuppressWarnings("deprecation")
		ConnectionProvider connectionProvider = sessionFactoryImplementor.getConnectionProvider();
		if (Stoppable.class.isInstance(connectionProvider)) {
			((Stoppable) connectionProvider).stop();
		}        
	}
	
	public static boolean persistManuscript(Manuscript m) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			session.save(m);
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static boolean linkManuscript(ManuscriptVerse mv, Integer page) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			mv.setPageNumber(page);
			session.merge(mv);
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}

	public static boolean persistManuscriptVerse(ManuscriptVerse mv) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			session.save(mv);
			session.flush();
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}

	public static boolean persistVerse(Verse v) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			session.save(v);
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static boolean flushObjects() {
		Session session = HibernateUtil.getSessionFactory().openSession();
		try {
			session.flush();
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static boolean clearObjects() {
		Session session = HibernateUtil.getSessionFactory().openSession();
		try {
			session.flush();
			session.clear();
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static boolean persistCopy(Integer i) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			session.save(i);
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static boolean persistDuplicate(Integer i) {
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			session.save(i);
			tx.commit();
		} catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
			return false;
		} finally {
			if (session.isOpen()) session.close();
		}
		return true;
	}
	
	public static List<Manuscript> retrieveManuscriptRange(int type, int name, int rangeend) {
		List<Manuscript> m = new ArrayList<Manuscript>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			org.hibernate.Query query;
			String q1 = "from bo.Manuscript where name >= :name and name <= :end";
			query = type==0 ? session.createQuery(q1) : session.createQuery(q1 + " and type = :type");
			if (type!=0) query.setParameter("type", type);
			query.setParameter("end", rangeend);
			query.setParameter("name", name);
			List<Manuscript> mss = query.list();
			for (Manuscript mm : mss) {
				m.add(mm);
			}
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return m;
	}
	
	public static List<String> printText(int book, String bookname, int chap, int verse, int mscount) {
		List<String> veret = new ArrayList<String>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			if (book != 0) {
				org.hibernate.Query query;
				String select = "from bo.Verse where book=:book";
				select = chap==0 ? select : select + " and chapter=:chap";
				query = session.createQuery(select);
				query.setParameter("book", book);
				String header = mscount+" Selected Manuscripts Containing " + bookname.toUpperCase();
				
				if (chap!=0) {
					query.setParameter("chap",chap);
					header = header + " " + chap;
				}
				
				List<Verse> vv = query.list();
				if (verse==0 || verse==99) {
					veret.add(header + "...");
					for (int i = 0; i < 6; ++i) {
						veret.add("v"+(i+1)+": "+vv.get(i).getText());
					}
					veret.add("... (" + (vv.size() - 6) + " verses not shown) ...");
				}
				else {
					veret.add(header+":"+verse+"...");
					veret.add("v"+verse+": "+vv.get(verse-1).getText());
				}
			}
			else {
				veret.add(mscount + " Manuscripts Containing the Entire New Testament");
			}
			
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return veret;
	}
	
	public static Comparator<Map.Entry<Manuscript, Integer>> uglyC = new Comparator<Map.Entry<Manuscript, Integer>>() {

		public int compare(Map.Entry<Manuscript, Integer> m1, Map.Entry<Manuscript, Integer> m2) {
			int typeComp = m1.getKey().getCentury().compareTo(m2.getKey().getCentury());
			if (typeComp == 0) {
				typeComp = m1.getKey().getType().compareTo(m2.getKey().getType());
				if (typeComp ==0) {
					return m1.getKey().getName().compareTo(m2.getKey().getName());
				}
			}
			return typeComp;
		}

	};
	
	public static List<Map.Entry<Manuscript,Integer>> retrieveManuscriptVersesRange(int book, int chap, int verse, int cbeg, int cend, Boolean pap, Boolean maj, Boolean min, Boolean lect, Boolean partialALL) {
		List<Map.Entry<Manuscript, Integer>> mv = new ArrayList<Map.Entry<Manuscript,Integer>>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			org.hibernate.Query query;
			if (cend == 1) cend=20;
			
			//ENTIRE NT
			if (book==0) {
				query = session.createQuery("select id.manuscript.id.manuscriptType as type, id.manuscript.id.manuscriptName as name "
						+ "from bo.ManuscriptVerse "
						+ "group by id.manuscript.id.manuscriptType, id.manuscript.id.manuscriptName "
						+ "having count(*) = 7957");
				List<Object[]> mss = query.list();
				
				for (Object[] mm : mss) {
					Manuscript.ManuscriptId mid = new Manuscript((Integer)mm[0], (Integer)mm[1]).getId();
					Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
					if (msCheck(m,cbeg,cend,pap,maj,min,lect)) mv.add(new SimpleEntry<>(m,null));
				}
				mv.sort(uglyC);
			}
			
			//not entire NT
			else {
				//entire book
				Convert c = new Convert();
				c.populateStructure();
				ArrayList<Integer> bookvcount = c.structure.get(new Convert().books.get(book - 1));
				
				if (chap==0) {
					Integer numv = 0;
					for (Integer i : bookvcount) numv+=i;
					
					String q = "select id.manuscript.id.manuscriptType as type, id.manuscript.id.manuscriptName as name "
							+ "from bo.ManuscriptVerse "
							+ "where id.verse.id.book = " + book
							+ "group by id.manuscript.id.manuscriptType, id.manuscript.id.manuscriptName";
					q = partialALL ? q : q + " having count(*) = " + numv;
					query = session.createQuery(q);
					List<Object[]> mss = query.list();
					for (Object[] mm : mss) {
						Manuscript.ManuscriptId mid = new Manuscript((Integer)mm[0], (Integer)mm[1]).getId();
						Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
						if (msCheck(m,cbeg,cend,pap,maj,min,lect)) mv.add(new SimpleEntry<>(m,null));
					}
					
					mv.sort(uglyC);
				}
				//not entire book
				else {
								
					//entire chapter
					if (verse==0) {
						Integer numvinc = bookvcount.get(chap-1);
						String q = "select id.manuscript.id.manuscriptType as type, id.manuscript.id.manuscriptName as name "
								+ "from bo.ManuscriptVerse "
								+ "where id.verse.id.book = " + book
								+ "and id.verse.id.chapter = " + chap
								+ "group by id.manuscript.id.manuscriptType, id.manuscript.id.manuscriptName";
						q = partialALL ? q : q + " having count(*) = " + numvinc;
						query = session.createQuery(q);
						List<Object[]> mss = query.list();
						for (Object[] mm : mss) {
							Manuscript.ManuscriptId mid = new Manuscript((Integer)mm[0], (Integer)mm[1]).getId();
							Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
							if (msCheck(m,cbeg,cend,pap,maj,min,lect)) mv.add(new SimpleEntry<>(m,null));
						}
						
						mv.sort(uglyC);
								
					}
					
					//single verse
					else {
						String q = "from bo.ManuscriptVerse "
								+ "where id.verse.id.book = " + book
								+ "and id.verse.id.chapter = " + chap
								+ "and id.verse.id.verse = " + verse;
						query = session.createQuery(q);
						
						List<ManuscriptVerse> allmvs = query.list();
						allmvs.sort(ManuscriptVerse.mvComparator);
						for (ManuscriptVerse mvs : allmvs) {
							Manuscript currMs= mvs.getManuscript();
							Integer currPg=mvs.getPageNumber();
							Entry<Manuscript,Integer> mspg=new SimpleEntry<>(currMs,currPg);
							if (msCheck(currMs, cbeg, cend, pap, maj, min, lect)) mv.add(mspg);
						}
					}
				}
			}
						
			for (Entry<Manuscript,Integer> q : mv) {
				System.out.println(q.getKey().getType()+", "+q.getKey().getName()+" cent: " + q.getKey().getCentury()+" page: "+q.getValue());
			}
			
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return mv;
	}
	
	public static List<Verse> getMsVerses(int type, int name) {
		List<Verse> vss = new ArrayList<Verse>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			Manuscript.ManuscriptId mid = new Manuscript(type, name).getId();
			Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
			for (ManuscriptVerse mv : m.getManuscriptVerses()) {
				vss.add(mv.getVerse());
			}
			vss.sort(Verse.verseComparator);
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return vss;
	}
	
	public static List<Manuscript> getCopies(int type, int name) {
		List<Manuscript> mss = new ArrayList<Manuscript>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			Manuscript.ManuscriptId mid = new Manuscript(type, name).getId();
			Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
			for (Integer mc : m.getCopies()) {
				Manuscript.ManuscriptId othermid = new Manuscript(type, mc).getId();
				Manuscript otherm = (Manuscript)session.get(Manuscript.class, othermid);
				mss.add(otherm);
			}
			mss.sort(Manuscript.manuscriptComparator);
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return mss;
	}
	
	public static List<Integer> getDuplicates(int type, int name) {
		List<Integer> mss = new ArrayList<Integer>();
		Session session = HibernateUtil.getSessionFactory().openSession();
		Transaction tx = session.getTransaction();
		try {
			tx.begin();
			Manuscript.ManuscriptId mid = new Manuscript(type, name).getId();
			Manuscript m = (Manuscript)session.get(Manuscript.class, mid);
			for (Integer mc : m.getDuplicates()) {
				mss.add(mc);
			}
			tx.commit();
		}
		catch (Exception e) {
			tx.rollback();
			e.printStackTrace();
		}
		finally {
			if (session.isOpen()) session.close();
		}
		return mss;
	}
	
	public static Boolean msCheck(Manuscript currMs, int cbeg, int cend, Boolean pap, Boolean maj, Boolean min, Boolean lect) {
		if(currMs.getCentury()>=cbeg && currMs.getCentury()<=cend) {
			if ((currMs.getType()==1)&&pap) return true;
			if ((currMs.getType()==2)&&maj) return true;
			if ((currMs.getType()==3)&&min) return true;
			if ((currMs.getType()==4)&&lect) return true;
		}
		return false;
	}
}