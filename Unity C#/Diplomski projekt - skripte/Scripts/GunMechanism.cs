using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GunMechanism : MonoBehaviour
{
    // Start is called before the first frame update

    Transform BarrelStart;
    Transform BarrelEnd;
    Vector3 ShotDir;
    public float BulletSpeed = 10;
    LineRenderer LaserPointer;

    void Start()
    {
        BarrelStart = this.transform.Find("BarrelStart");
        BarrelEnd = this.transform.Find("BarrelEnd");
        LaserPointer = transform.Find("Line").GetComponent<LineRenderer>();
        LaserPointer.positionCount = 2;
        LaserPointer.startWidth = 0.01f;
        LaserPointer.endWidth = 0.01f;
    }

    // Update is called once per frame
    void Update()
    {
        ShotDir = (BarrelEnd.position - BarrelStart.position).normalized;
        //Debug.DrawLine (BarrelEnd.position, BarrelEnd.position + ShotDir * 10, Color.red, 0.1f);
        LaserPointer.SetPosition(0, BarrelEnd.transform.position);

        //Layer "player" je postavljen pod mjesto 8. Bit shiftamo layerMask za mjesto 8
        int layerMask = 1 << 8;
        //ovaj layerMask bi sada ocitavao sudare samo za layer 8, sto znaci da invertiramo da bi ocitavalo sve osim igraca
        layerMask = ~layerMask;

        //10 jer ako je manje crtamo laser do sudara
        RaycastHit hit;
        if (Physics.Raycast(BarrelEnd.position, ShotDir, out hit, 10, layerMask)) {
            LaserPointer.SetPosition(1, BarrelEnd.position + ShotDir * hit.distance);
        } else {
            LaserPointer.SetPosition(1, BarrelEnd.position + ShotDir * 10);
        }
/*
        // Does the ray intersect any objects excluding the player layer
        if (Physics.Raycast(BarrelEnd.position, ShotDir, out hit, Mathf.Infinity, layerMask))
        {
            Debug.DrawRay(BarrelEnd.position, ShotDir * hit.distance, Color.yellow);
            Debug.Log("Did Hit");
        }*/
    }

    public void Shoot() {
        GameObject bullet = (GameObject) Instantiate(Resources.Load("Prefabs/Bullet"), BarrelEnd.position, Quaternion.Euler(ShotDir));
        bullet.GetComponent<BulletMechanism>().SetValues(BulletSpeed, ShotDir);
    }
}
