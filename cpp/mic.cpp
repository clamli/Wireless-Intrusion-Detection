#include "portaudio.h"
#include <stdio.h>
#include "cstring"
#include <mongoc.h>
#include <bson.h>

#define SAMPLE_RATE (32000)

typedef struct
{
    float *nums;
    uint32_t len;
}   
paTestData;
/* This routine will be called by the PortAudio engine when audio is needed.
   It may called at interrupt level on some machines so don't do anything
   that could mess up the system like calling malloc() or free().
*/ 
static int patestCallback( const void *inputBuffer, void *outputBuffer,
                           unsigned long framesPerBuffer,
                           const PaStreamCallbackTimeInfo* timeInfo,
                           PaStreamCallbackFlags statusFlags,
                           void *userData )
{
    /* Cast data passed through stream to our structure. */
    paTestData *data = (paTestData*)userData;
    float *in = (float*)inputBuffer;
    unsigned int i;
    unsigned int j;
    (void) outputBuffer; /* Prevent unused variable warning. */
    //printf("\nhellocb\n");
    for( i=0; i<framesPerBuffer; i++ )
    {
        for (j = 0; j < 8; ++j) {
            data->nums[(data->len)++] = *in++;
        }
    }
    return 0;
}

static paTestData data;

int main() {    
    // mongodb init...
    const char *uri_string = "mongodb://192.168.1.144:27017/";
    mongoc_uri_t *uri;
    mongoc_client_t *client;
    mongoc_database_t *database;
    mongoc_collection_t *collection;
    bson_t *command, reply, *insert;
    bson_error_t error;
    char *str;
    bool retval;
    /*
     * Required to initialize libmongoc's internals
     */
    mongoc_init ();
    /*
     * Safely create a MongoDB URI object from the given string
     */
    uri = mongoc_uri_new_with_error (uri_string, &error);
    if (!uri) {
        fprintf (stderr,
                "failed to parse URI: %s\n"
                "error message:       %s\n",
                uri_string,
                error.message);
        return EXIT_FAILURE;
    }
    /*
     * Create a new client instance
     */
    client = mongoc_client_new_from_uri (uri);
    if (!client) {
        return EXIT_FAILURE;
    }
    /*
     * Register the application name so we can track it in the profile logs
     * on the server. This can also be done from the URI (see other examples).
     */
    mongoc_client_set_appname (client, "connect-example");
    /*
     * Get a handle on the database "db_name" and collection "coll_name"
     */
    database = mongoc_client_get_database (client, "test_db");
    collection = mongoc_client_get_collection (client, "test_db", "users");




    // init ends


    PaError err = Pa_Initialize();        
    int num = Pa_GetDeviceCount();
    printf("Device num: %d\n", num);
    for (int i = 0; i < num; ++i) {
        auto deviceInfo = Pa_GetDeviceInfo(i);
        printf("%s\n", deviceInfo->name);
        printf("maxInputChannel: %d\n", deviceInfo->maxInputChannels);
    }
    if (err != paNoError) {
        printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
        return -1;
    }        
    PaStream *stream;

    PaStreamParameters inputParameters;
    memset( &inputParameters, '\0', sizeof( inputParameters ));
    //bzero( &inputParameters, sizeof( inputParameters ) ); //not necessary if you are filling in all the fields
    inputParameters.channelCount = 8;
    inputParameters.device = 3;
    inputParameters.hostApiSpecificStreamInfo = NULL;
    inputParameters.sampleFormat = paFloat32; 
    inputParameters.suggestedLatency = Pa_GetDeviceInfo(3)->defaultLowInputLatency ;
    inputParameters.hostApiSpecificStreamInfo = NULL; //See you specific host's API docs for info on using this field
    /* Open an audio I/O stream. */
    err = Pa_OpenStream( 
                            &stream,
                                &inputParameters,          /* 8 input channels */
                                NULL,          /* no output */
                                SAMPLE_RATE,
                                2048,        /* frames per buffer, i.e. the number
                                                   of sample frames that PortAudio will
                                                   request from the callback. Many apps
                                                   may want to use
                                                   paFramesPerBufferUnspecified, which
                                                   tells PortAudio to pick the best,
                                                   possibly changing, buffer size.*/
                                paNoFlag,                                                   
                                patestCallback, /* this is your callback function */
                                &data ); /*This is a pointer that will be passed to
                                                   your callback*/
    if (err != paNoError) {
        printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
        return -1;
    }    
    float max = 0;    
    int64_t cnt = 0;
    data.nums = new float[SAMPLE_RATE*4*8]; 
    while (cnt < 1000) {
        ++cnt;
    
        data.len = 0;
        printf("%" PRId64 " th loop\n", cnt);
        err = Pa_StartStream( stream );
        if (err != paNoError) {
            printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
            return -1;
        }

        /* Sleep for several seconds. */
        Pa_Sleep(3*1000);
        err = Pa_StopStream( stream );
        if (err != paNoError) {
         printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
         return -1;
        }
        printf("Length is: %" PRIu32 "\n", data.len );
        
        /*for (auto i = 0; i < 60; i = i + 1) {
            printf("%f  ", data.nums[i]);
        }
        printf("\n");*/

        bson_t *document;
        document = bson_new ();
        BSON_APPEND_INT64(document, "wave_id", cnt);
        BSON_APPEND_BINARY(document, "data", BSON_SUBTYPE_USER, (uint8_t*) data.nums, 4*data.len);
        
        /*max = 0;
        for (auto i = 0; i < data.len; ++i) {
            if (max < data.nums[i]) max = data.nums[i];            
        }
        printf("maximum is: %f\n", max);*/

        printf("start sending\n");
        if (!mongoc_collection_insert_one (collection, document, NULL, NULL, &error)) {
            fprintf (stderr, "%s\n", error.message);
        }
        printf("end sending\n");
        bson_destroy(document);


    }    
    delete[] data.nums;


    err = Pa_Terminate();
    if (err != paNoError) {
        printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
        return -1;
    }

    /*
     * Release our handles and clean up libmongoc
     */
    mongoc_collection_destroy (collection);
    mongoc_database_destroy (database);
    mongoc_uri_destroy (uri);
    mongoc_client_destroy (client);
    mongoc_cleanup ();

    return 0;
}