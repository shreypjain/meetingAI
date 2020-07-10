//
//  ContentView.swift
//  meetingAI
//
//  Created by Shrey Jain on 7/9/20.
//  Copyright © 2020 Shrey Jain. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @ObservedObject var audioRecorder: AudioRecorder
    var body: some View {
        VStack {
            RecordingsList(audioRecorder: audioRecorder)
            if audioRecorder.recording == false {
                Button(action: {print("Start recording")}) {
                    Image(systemName: "circle.fill")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 100, height: 100)
                        .clipped()
                        .foregroundColor(.red)
                        .padding(.bottom, 40)
                }
            } else {
                Button(action: {print("Stop recording)")}) {
                    Image(systemName: "stop.fill")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 100, height: 100)
                        .clipped()
                        .foregroundColor(.red)
                        .padding(.bottom, 40)
                }
            }
        }
    .navigationBarTitle("Voice recorder")
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView(audioRecorder: AudioRecorder())
    }
}
