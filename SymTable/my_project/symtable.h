#include<iostream>
#include <bits/stdc++.h>

using namespace std;

class Symtable{
    public:
	const char* key;
	const char* value;
	Symtable *next;
    typedef Symtable* SymTable_t;
    SymTable_t SymtableNew();
    void SymTable_free (Symtable** oSymTable);
    int SymTable_getLength (SymTable_t oSymTable);
    void SymTable_map (SymTable_t oSymTable,void (*pfApply) (const char *pcKey,const void *pvValue,void *pvExtra),const void *pvExtra);
    void map_example(const char *pcKey,const void *pvValue,void *pvExtra);
    void display(SymTable_t oSymTable);
    int SymTable_contains (SymTable_t oSymTable,const char *pcKey);
    int SymTable_put(Symtable* oSymTable,const char* pcKey,const char* pvValue);
    const char *SymTable_get (SymTable_t oSymTable, const char *pcKey);
    void SymTable_remove (Symtable** oSymTable,const char *pcKey);
    void SymTable_replace (SymTable_t oSymTable,const char *pcKey,const char *pvValue);

};