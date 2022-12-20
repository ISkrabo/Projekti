using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraDetector : MonoBehaviour
{
    GameObject camera;
    GameObject leftLight;
    GameObject rightLight;
    GameObject EventHandler;
    GameObject MainAimVisiblePoint;

    private Color original;
    private Color highlight = Color.green;
    // Start is called before the first frame update
    void Start()
    {
        camera = GameObject.FindGameObjectWithTag("MainCamera");
        EventHandler = GameObject.FindGameObjectWithTag("EventHandler");
        leftLight = GameObject.Find("LeftLight");
        rightLight = GameObject.Find("RightLight");
        MainAimVisiblePoint = GameObject.Find("MainAimVisiblePoint");
        original = MainAimVisiblePoint.GetComponent<MeshRenderer>().material.color;
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit ray;
        Physics.Raycast(camera.transform.position, camera.transform.forward, out ray);
        if (ray.collider != null && ray.collider.name == "MainAim") { //ray.collider provjera null za izbjegavanje errora
            EventHandler.GetComponent<EventsSystem>().CameraDetector = true;
            leftLight.GetComponent<LightScript>().CameraDetector = true;
            MainAimVisiblePoint.GetComponent<MeshRenderer>().material.color = highlight;
        } else {
            EventHandler.GetComponent<EventsSystem>().CameraDetector = true;
            rightLight.GetComponent<LightScript>().CameraDetector = false;
            MainAimVisiblePoint.GetComponent<MeshRenderer>().material.color = original;
        }
    }
}
