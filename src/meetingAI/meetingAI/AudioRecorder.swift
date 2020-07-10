//
//  AudioRecorder.swift
//  meetingAI
//
//  Created by Shrey Jain on 7/9/20.
//  Copyright © 2020 Shrey Jain. All rights reserved.
//

import Foundation
import SwiftUI
import Combine
import AVFoundation

class AudioRecorder: ObservableObject {
    let objectWillChange = PassthroughSubject<AudioRecorder, Never>()
    var audioRecorder: AVAudioRecorder!
    
    var recording = false {
        didSet {
            objectWillChange.send(self)
        }
    }
    func startRecording() {
        let recordingSession = AVAudioSession.sharedInstance()
        do {
            try recordingSession.setCategory(.playAndRecord, mode: .default)
            try recordingSession.setActive(true)
        } catch {
            print("Failed to set up recording session")
        }
        let documentPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let audioFilename = documentPath.appendingPathComponent("\(Date().toString(dateFormat: "dd-MM-YY_'at'_HH:mm:ss")).mp3")
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
    }
    do {
        audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
        audioRecorder.record()

        recording = true
    } catch {
        print("Could not start recording")
    }
    Button(action: {self.audioRecorder.startRecording()}) {
        Image(systemName: "circle.fill")
            //...
    }
    Button(action: {self.audioRecorder.stopRecording()}) {
        Image(systemName: "stop.fill")
            //...
    }
    func stopRecording() {
        audioRecorder.stop()
        recording = false
    }
}
extension Date
{
    func toString( dateFormat format  : String ) -> String
    {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = format
        return dateFormatter.string(from: self)
    }

}
