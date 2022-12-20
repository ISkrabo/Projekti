using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Tobii.XR;

//TobiiXRCustom se bavi radom s ocima (kroz HTC vive)

[DefaultExecutionOrder(-10)]
public class TobiiXRCustom : MonoBehaviour
{
    public TobiiXR_Settings Settings;

    private bool stopwatchStarted;
    private float stopwatchTimer;
    
    private float blinkDuration = 0f;

    private float blinkFloor = 0f;
    private float blinkCurr = 0f;
    private float blinkPrev = 0f;

    private GameObject EventHandler;
    private void Awake()
    {
        TobiiXR.Start(Settings); 
    }



    // Start is called before the first frame update
    void Start()
    {
        EventHandler = GameObject.FindGameObjectWithTag("EventHandler");
    }

    // Update is called once per frame
    void Update()
    {
        
        var test = TobiiXR.GetEyeTrackingData(TobiiXR_TrackingSpace.Local);

        //if (test.IsLeftEyeBlinking && !test.IsRightEyeBlinking) Debug.Log("Lijevo oko");

        //if (!test.IsLeftEyeBlinking && test.IsRightEyeBlinking) Debug.Log("Desno oko");
        
        if (test.IsLeftEyeBlinking || test.IsRightEyeBlinking) {
            if (blinkFloor == 0f) {
                blinkFloor = test.Timestamp; 
                blinkPrev = test.Timestamp; 
            }
            blinkCurr = test.Timestamp; 
            //0.2f je odabrano testirajuci timestamp-ove tokom "treptaja" (zatvorenih ociju)
            if (blinkCurr - blinkPrev < 0.2f) {
                blinkPrev = blinkCurr; 
            } else {
                blinkDuration = blinkPrev - blinkFloor;
                blinkFloor = blinkCurr;
                blinkPrev = blinkCurr;

                if (blinkDuration > 0f) EventHandler.GetComponent<EventsSystem>().AddBlink(blinkDuration);
            }
        } 

        if (stopwatchStarted) {
            //fokus na metu postoji
            if (TobiiXR.FocusedObjects.Count > 0) {
                var focusedGameObj = TobiiXR.FocusedObjects[0].GameObject;
            } else {
                stopwatchTimer += Time.deltaTime;
                
            }
        }
    }

    public void Stopwatch(bool start) {
        stopwatchStarted = start;
        stopwatchTimer = 0.0f;
    }
}
