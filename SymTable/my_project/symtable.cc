#include "symtable.h"

Symtable* Symtable::SymtableNew() {	
	Symtable* new_node = (Symtable*) malloc(sizeof(Symtable));
	if(new_node==NULL) {
		cout<<"Not Enough Memory to create Linked List...";
	}
	return new_node;
}

void Symtable::SymTable_free(Symtable** oSymTable) {
	SymTable_t temp = SymtableNew();
	SymTable_t curr = SymtableNew();
	temp = *oSymTable;

      while(temp != NULL) {
        *oSymTable = temp->next;
        temp->next=NULL;
        free(temp);
        temp=*oSymTable;
      }
      cout<<"All nodes are deleted successfully..."<<endl; 
}

int Symtable::SymTable_getLength (SymTable_t oSymTable){
	if (oSymTable == NULL)
      return 0;
   	return 1 + SymTable_getLength(oSymTable->next);
}

void Symtable::SymTable_map (SymTable_t oSymTable,void (*pfApply) (const char *pcKey,const void *pvValue,void *pvExtra),const void *pvExtra){
	SymTable_t current = SymtableNew();
	current=oSymTable;
	while(current!=NULL) {
		pfApply(current->key,current->value,(void*)pvExtra);
		current= current->next;
	}
}

int Symtable::SymTable_put(Symtable* oSymTable,const char* pcKey,const char* pvValue) {
	SymTable_t current = oSymTable; 
    while (current!= NULL) { 	
		if (string(current->key) == string(pcKey)) {
			if (string(current->value) != string(pvValue)) {
				cout << "Replaced Value from " << current->value << " to " << pvValue<<endl;
				return 1;
			}
			return 1;
		}           
        current = current->next; 
    } 
    SymTable_t curr = oSymTable;
    while(curr->next!=NULL)
    	curr=curr->next;
    Symtable* new_node = SymtableNew();
	new_node->key = pcKey;
	new_node->value = pvValue;
	new_node->next = NULL;
	curr->next=new_node;
    return 0; 
}

int Symtable::SymTable_contains (SymTable_t oSymTable,const char *pcKey) {
	SymTable_t current = oSymTable; 
    while (current!= NULL) {    	
        if (string(current->key) == string(pcKey)) {
        	return 1;
		}            
        current = current->next; 
    } 
    return 0;
}

void Symtable::SymTable_replace(SymTable_t oSymTable,const char *pcKey,const char *pvValue) {
	Symtable* current = oSymTable; 
    while (current!= NULL) {  	
        if (string(current->key) == string(pcKey)) {
        	current->value=pvValue;
        	cout<<"Replaced Value for key :"<<pcKey<<endl;
        	break;
		}            
        current = current->next; 
    } 
    if(current==NULL) {
    	cout<<"Element not present in SymTable"<<endl;
	}  
}

const char* Symtable::SymTable_get(Symtable* oSymTable, const char *pcKey) {
	Symtable* current = oSymTable; 
    while (current!= NULL) {
        if (string(current->key) == string(pcKey)) {
        	return current->value;
		}            
        current = current->next; 
    } 
    return NULL;
}

void Symtable::SymTable_remove (Symtable** oSymTable,const char *pcKey) {
	Symtable* temp = *oSymTable;
    Symtable* prev = NULL;
      
    if(temp != NULL && string(temp->key) == string(pcKey)) {
    	
        //temp=oSymTable;
		*oSymTable=temp->next; 
		temp->next=NULL;
        free(temp);		 
		cout<<"Node with Key "<<pcKey<<" removed"<<endl;        
        
    }
    else {
	    while(temp != NULL && string(temp->key) != string(pcKey)) {
	        prev = temp;
	        temp = temp->next;
	    }
	    if(temp == NULL) {
	    	cout<<"Element with key "<<pcKey<<" not present in linked list"<<endl;
		}
	    prev->next = temp->next;
	    temp->next=NULL;
	    delete temp;
	    cout<<"Node with Key "<<pcKey<<" removed"<<endl;
	}
}

void map_example(const char *pcKey,const void *pvValue,void *pvExtra) {
	cout<<"Entered Map Function..."<<endl;
	cout<<pcKey<<endl;
	cout<<pvValue<<endl;
}

void Symtable::display(Symtable* oSymTable) {
	SymTable_t current = oSymTable; 
	if(current==NULL) {
		cout<<"List is Empty..."<<endl;
	}
	else {
			while (current!= NULL) { 
		        cout<<current->key<<endl;
		        cout<<current->value<<endl;
		        current = current->next; 
		    } 
	} 
}