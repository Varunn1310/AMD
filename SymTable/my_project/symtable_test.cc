#include "symtable.cc"
#include <gtest/gtest.h>

// Demonstrate some basic assertions.
TEST(SymtableTest, BasicAssertions) {
  Symtable s;
  Symtable* start = s.SymtableNew();
  //test for SymtableNew()
	ASSERT_TRUE(start != NULL);

  start->key = "foo";
	start->value = "int";
	start->next = NULL;
	start->SymTable_free(&start);
  //test for SymTable_free()
  ASSERT_TRUE(start == NULL);

  Symtable* start1 = s.SymtableNew();
	start1->key = "foo";
	start1->value = "int";
	start1->next = NULL;
  //test for SymTable_getLength()
	ASSERT_EQ(start1->SymTable_getLength(start1), 1);

  s.SymTable_map(start1, &map_example, NULL);
  //test for SymTable_contains()
	ASSERT_EQ(s.SymTable_contains(start1, "fiii"), 0);
  //test for SymTable_put
	ASSERT_EQ(s.SymTable_put(start1,"fii","int"), 0);

	//display(start1);
	cout << s.SymTable_get(start1, "fii") << endl;
  //test for SymTable_get
	ASSERT_TRUE(s.SymTable_get(start1, "fii")== string("int"));

	s.SymTable_remove(&start1, "foo");
  //test for SymTable_remove
  ASSERT_EQ(s.SymTable_contains(start1, "foo"), 0);
	s.display(start1);
	s.SymTable_replace(start1, "fii", "floor");
  //test for SymTable_replace
	ASSERT_EQ(string(start1->value), "floor");
}
