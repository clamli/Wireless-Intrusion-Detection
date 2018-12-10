#include <mongoc.h>
#include <bcon.h>
#include <stdio.h>

static void
print_query_count (mongoc_collection_t *collection, bson_t *query)
{
   bson_error_t error;
   int64_t count;

   count = mongoc_collection_count (
      collection, MONGOC_QUERY_NONE, query, 0, 0, NULL, &error);

   if (count < 0) {
      fprintf (stderr, "Count failed: %s\n", error.message);
   } else {
      printf ("%" PRId64 " documents counted.\n", count);
   }
}

int main() {
    
}