#define PI 3.1415926538
in vec2 fragCoord;
out vec4 fragColor;
vec3 arr[16];
vec2 uvArr[16];
vec3 evalArr[16];
vec3 camPos = vec3(5.0,5.0,7.0);
float projection = 2.0;
float minU = 0.0;
float maxU = 1.0;
float minV = 0.0;
float maxV = 1.0;
vec4 fragColorF = vec4(0.0,0.0,0.0,1.0);



vec3 normalize_m(vec3 vec) {
    float mag = length(vec);
    if (mag == 0.0) 
    {
        return vec3(0,0,0);
    }
    return normalize(vec);
}
vec2 normalize_m(vec2 vec) {
    float mag = length(vec);
    if (mag == 0.0) 
    {
        return vec2(0,0);
    }
    return normalize(vec);
}
vec3 lerp2(vec3 a, vec3 b,float t) {
    return vec3((b.x - a.x) * t + a.x, (b.y - a.y) * t + a.y, (b.z - a.z) * t + a.z);
}
vec3 lerp3(vec3 a,vec3 b,vec3 c,float t) {
    return lerp2(lerp2(a,b,t),lerp2(b,c,t),t);
}
vec3 lerp4(vec3 a,vec3 b, vec3 c, vec3 d, float t) {
    return lerp2(lerp3(a,b,c,t),lerp3(b,c,d,t),t);
}
vec3 getRay(vec3 pos) {
    return normalize(pos - camPos);
}

vec3 subtract(vec3 v1, vec3 v2) {
    return vec3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
}
vec3 add(vec3 v1, vec3 v2) {
    return vec3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
}
float lenDiff(vec3 v1, vec3 v2) {
    return abs(length(v1) - length(v2));
}
vec3[2] getBoundingBox(vec3[16] pts) {
    vec3 boxMin = vec3(1,1,1)*10000000.0;
    vec3 boxMax = vec3(1,1,1)*-10000000.0;
    for (int i = 0; i < pts.length(); i++) {
        if (pts[i].x < boxMin.x) {
            boxMin.x = pts[i].x;
        }
        if (pts[i].y < boxMin.y) {
            boxMin.y = pts[i].y;
        }
        if (pts[i].z < boxMin.z) {
            boxMin.z = pts[i].z;
        }
        if (pts[i].x > boxMax.x) {
            boxMax.x = pts[i].x;
        }
        if (pts[i].y > boxMax.y) {
            boxMax.y = pts[i].y;
        }
        if (pts[i].z > boxMax.z) {
            boxMax.z = pts[i].z;
        }
    }
    return vec3[2] (boxMin, boxMax);
}
vec3[2] getBoundingBoxDir(vec3[16] pts) {
    vec3 boxMin = vec3(1,1,1)*10000000.0; // dir
    vec3 boxMax = vec3(1,1,1)*-10000000.0; // dir
    for (int i = 0; i < pts.length(); i++) {
        vec3 dir = normalize(pts[i] - camPos);
        if (dir.x < boxMin.x) {
            boxMin.x = dir.x;
        }
        if (dir.y < boxMin.y) {
            boxMin.y = dir.y;
        }
        if (dir.z < boxMin.z) {
            boxMin.z = dir.z;
        }
        if (dir.x > boxMax.x) {
            boxMax.x = dir.x;
        }
        if (dir.y > boxMax.y) {
            boxMax.y = dir.y;
        }
        if (dir.z > boxMax.z) {
            boxMax.z = dir.z;
        }
    }
    return vec3[2] (boxMin, boxMax);
}
bool isInside(vec3 _pos, vec3 _min, vec3 _max) {
    return _min.x < _pos.x && _min.y < _pos.y && _min.z < _pos.z && _max.x > _pos.x && _max.y > _pos.y && _max.z > _pos.z;
}
vec3 evaluate(float u, float v) {
    vec3 a = lerp4(arr[0],arr[1],arr[2],arr[3],u);
    vec3 b = lerp4(arr[4],arr[5],arr[6],arr[7],u);
    vec3 c = lerp4(arr[8],arr[9],arr[10],arr[11],u);
    vec3 d = lerp4(arr[12],arr[13],arr[14],arr[15],u);
    return lerp4(a,b,c,d,v);
}
void start() {
    arr[0] = vec3(0, 0, 0);
    arr[1] = vec3(1, 0, 1);
    arr[2] = vec3(2, 0, -1);
    arr[3] = vec3(3, 0, 0);

    arr[4] = vec3(0, 1, 0);
    arr[5] = vec3(1, 1, 1);
    arr[6] = vec3(2, 1, -1);
    arr[7] = vec3(3, 1, 0);

    arr[8] = vec3(0, 2, 0);
    arr[9] = vec3(1, 2, 1);
    arr[10] = vec3(2, 2, -1);
    arr[11] = vec3(3, 2, 0);

    arr[12] = vec3(0, 3, 0);
    arr[13] = vec3(1, 3, 1);
    arr[14] = vec3(2, 3, -1);
    arr[15] = vec3(3, 3, 0);
    
    uvArr[0] = vec2(0,0);
    uvArr[1] = vec2(0.33,0);
    uvArr[2] = vec2(0.66,0);
    uvArr[3] = vec2(1,0);
    
    uvArr[4] = vec2(0,.33);
    uvArr[5] = vec2(0.33,.33);
    uvArr[6] = vec2(0.66,.33);
    uvArr[7] = vec2(1,.33);
    
    uvArr[8] = vec2(0,.66);
    uvArr[9] = vec2(0.33,.66);
    uvArr[10] = vec2(0.66,.66);
    uvArr[11] = vec2(1,.66);
    
    uvArr[12] = vec2(0,1);
    uvArr[13] = vec2(0.33,1);
    uvArr[14] = vec2(0.66,1);
    uvArr[15] = vec2(1,1);
    
    for (int i = 0; i < uvArr.length(); i++) {
        evalArr[i] = evaluate(uvArr[i].x, uvArr[i].y);
    }
}
vec4 colorG = vec4(0,0,0,1);
void generatePoints(out vec3[32] outArr, out vec2[32] outUvArr) {
    float n = sqrt(32.0);
    int i = 0;
    float change = 1.0 / (n - 1.0);
    
    for (float v = 0.0; v <= 1.0; v += change) {
        for (float u = 0.0; u <= 1.0; u += change) {
            outUvArr[i] = vec2(u,v);
            outArr[i] = evaluate(u,v);
            if (i >= 15) {
                colorG = vec4(0,1,0,1);
            }
            i += 1;
        }
    }
} 
int getClosestPointIndexToRay(vec3[32] pts, vec3 origin, vec3 rayDir) 
{
   float closest = 100000000.0;
   int closestPtIndex = 0;
   for (int i = 0; i < pts.length(); i++) {
       //float dist = length(origin - pts[i]);
       //float rayDist = length(rayDir * dist);
       vec3 dir = normalize(pts[i] - origin);
       //vec3 rayDir = rayDir * dist;
       float len = length(dir - rayDir);
       if (len < closest) {
           closestPtIndex = i;
           closest = len;
       }
   }
   return closestPtIndex;
}
bool isValid(float u, float v) {
    return 0.0 <= u && u <= 1.0 && 0.0 <= v && v <= 1.0;
}

void render(vec2 fragCoord) {
    //getClosestPointIndexToRay(arr, vec3(0,0,0), normalize(vec3(fragCoord,1)));
}
bool iterate(float u, float v, vec3 camPos, vec3 targetDir, float offset, float marginOfError, int tries, out vec3 xyz, out vec2 uv) {
    //
    u = 1.0;
    v = 1.0;
    //
    xyz = vec3(0,0,0);
    uv = vec2(0,0);
    vec2 change = vec2(0,0);
    vec3 center = evaluate(u,v);
    float centerDiff = length(normalize(center - camPos) - targetDir);
    vec3 left;
    float leftDiff = centerDiff;
    vec3 right;
    float rightDiff = centerDiff;
    vec3 up;
    float upDiff = centerDiff;
    vec3 down;
    float downDiff = centerDiff;
    bool complete = false;
    float diffTotal = 0.0;
    bool rightValid = isValid(u+offset,v);
    bool leftValid = isValid(u-offset,v);
    bool upValid = isValid(u,v+offset);
    bool downValid = isValid(u,v-offset);
    vec2 lowChange = vec2(1000000,1000000);
    while(!complete) {
        rightValid = isValid(u+offset,v);
        leftValid = isValid(u-offset,v);
        upValid = isValid(u,v+offset);
        downValid = isValid(u,v-offset);
        diffTotal = 0.0;
        change = vec2(0,0);
        if (rightValid) {
            right = evaluate(u+offset,v) - camPos;
            downDiff = length(normalize(right) - targetDir);
            diffTotal += rightDiff;
        }
        if (leftValid) {
            left = evaluate(u-offset,v) - camPos;
            leftDiff = length(normalize(left) - targetDir);
            diffTotal += leftDiff;
        }
        if (upValid) {
            up = evaluate(u,v+offset) - camPos;
            upDiff = length(normalize(up) - targetDir);
            diffTotal += upDiff;
        }
        if (downValid) {
            down = evaluate(u,v-offset) - camPos;
            downDiff = length(normalize(down) - targetDir);
            diffTotal += downDiff;
        }
        diffTotal = 0.6;
        if (downValid && downDiff < centerDiff) {
            change.y -= diffTotal - downDiff;
        }
        if (upValid && upDiff < centerDiff) {
            change.y += diffTotal - upDiff;
        }
        if (leftValid && leftDiff < centerDiff) {
            change.x -= diffTotal - leftDiff;
        }
        if (rightValid && rightDiff < centerDiff) {
            change.x += diffTotal - rightDiff;
        }
        change = normalize_m(change) * offset;
        //
        
        //fragColorF = vec4(lerp2(vec3(1,0,0),vec3(0,0,1),t),1.0);
        //if (change.y > 0.0) {
            //fragColorF = vec4((change / 0.5) + vec2(0.5,0.5),0,1);
            //fragColorF = vec4(1.0,1.0,1.0,1.0);
        //}
        //if (change.x > change.y) {
            //fragColorF = vec4(1,1,0,1);
        //}
        //
        float newU = u + change.x;
        float newV = v + change.y;
        if (newU > maxU || newU < minU) {
            newU = u;
        }
        if (newV > maxV || newV < minV) {
            newV = v;
        }
        vec3 eval = evaluate(newU,newV);
        vec3 evalDir = normalize(eval - camPos);
        float dirDiff = length(evalDir - targetDir);
        if (dirDiff < marginOfError) {
            complete = false;
            xyz = eval;
            uv = vec2(newU, newV);
            return true;
        }
        if (tries <= 0) {
            complete = false;
            return false;
        }
        u = newU;
        v = newV;
        center = evaluate(newU,newV);
        centerDiff = dirDiff;
        tries -= 1;
    }
    return false;
}
// http://eecs.qmul.ac.uk/~gslabaugh/publications/euler.pdf
vec3 rotate(vec3 vec, float x, float y, float z) {
    mat3 matx = mat3(
        1, 0, 0,
        0, cos(x), -sin(x),
        0, sin(x), cos(x)
    );
    mat3 maty = mat3(
        cos(y), 0, sin(y),
        0, 1, 0,
        -sin(y), 0, cos(y)
    );
    mat3 matz = mat3(
        cos(z), -sin(z), 0,
        sin(z), cos(z), 0,
        0, 0, 1
    );
    return vec * matx * maty * matz;
}

void mainImage()
{
    start();
    vec3[32] m_Arr;
    vec2[32] m_uvArr;
    generatePoints(m_Arr, m_uvArr);
    mat3 rot_matrix = mat3(
    1,0,0,
    0,1,0,
    0,0,1
    );
    //rot_matrix = rotate(
    
    vec2 uv = fragCoord/iResolution.xy;
    //vec3 rayDir = normalize(vec3(uv,projection) * rot_matrix - vec3(0,0,0));
    vec3 rayDir = normalize(rotate(vec3(uv,projection),radians(35.0),radians(195.0),0.0) - vec3(0,0,0));
    vec3[] boundingBoxDir = getBoundingBoxDir(arr);
    bool hit = isInside(rayDir, boundingBoxDir[0], boundingBoxDir[1]);
    if (hit) {
        //fragColor = vec4(1.0,1.0,1.0,1.0);
        int nearPtIndex = getClosestPointIndexToRay(m_Arr, camPos, rayDir);
        
        vec2 uv = m_uvArr[nearPtIndex];
        vec2 uvPos;
        vec3 xyzPos;
        bool intersection = iterate(uv.x, uv.y, camPos, rayDir, 0.003, 0.002, 500, xyzPos, uvPos);
        if (intersection) {
            fragColor = vec4(uvPos.x,uvPos.y,0.0,1.0);
            //fragColor = vec4(float(nearPtIndex)/32.0,1.0,1.0,1.0);
        }
        else {
            fragColor = vec4(0.5,0.5,0.5,1.0);
            //fragColor = vec4(uv,0,1.0);
        }
    }
    else {
        fragColor = vec4(0.5,0.5,0.5,1.0);
    }
    //fragColor = vec4(evaluate(1.0,0.0),1);
    //fragColor = fragColorF;
    //fragColor = colorG;
    // Normalized pixel coordinates (from 0 to 1)
    //vec2 uv = fragCoord/iResolution.xy;
    //
    // Time varying pixel color
    //vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));
    //
    // Output to screen
    //fragColor = vec4(col,1.0);
}