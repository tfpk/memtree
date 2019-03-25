#include <stdlib.h>
#define DEPTH 3

struct treenode {
    struct treenode* l;
    struct treenode *r;
};

void tree(struct treenode *rel, int recurdown){
    rel->l = NULL;
    rel->r = NULL;
    if (recurdown == 0) return;
    rel->l = malloc(sizeof(struct treenode));
    tree(rel->l, recurdown - 1);
    rel->r = malloc(sizeof(struct treenode));
    tree(rel->r, recurdown - 1);
}

int main(){
    struct treenode *base = malloc(sizeof (struct treenode));
    tree(base, DEPTH);
    // break here!
    return 0;
}
